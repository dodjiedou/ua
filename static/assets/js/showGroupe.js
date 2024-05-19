document.addEventListener("DOMContentLoaded", function () {
    const page = document.getElementById("page");
    const lien = window.groupeLink;
    let hot = page.innerHTML;
    const show = `
<div>
<div class="alert alert-secondary mx-4" role="alert">
<span class="text-white">
    <strong>Inviter un membre, Editer les informations d'un membe, Supprimer les informations d'un membre</strong> 
   
    Gérer les membre de votre groupe!
</span>
</div>








<div class="row">
<div class="col-12">
    <div class="card mb-4 mx-4">
        <div class="card-header pb-0">
            <div class="d-flex flex-row justify-content-between">
                <div>
                    <h5 class="mb-0">Tous les membres</h5>
                </div>
                <a href="#" class="btn bg-gradient-primary btn-sm mb-0" type="button" data-action="invite"data-bs-toggle="modal"
                title="Détails du groupe"
                                    
                    data-bs-target="#partageModal">Inviter un membre</a>
            </div>
        </div>
        <div class="card-body px-0 pt-0 pb-2">
            <div class="table-responsive p-0">
                <table class="table align-items-center mb-0">
                    <thead>
                        <tr>
                            <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                                Membre
                            </th>
                            
                           
                            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 d-none d-md-table-cell">
                                Contact
                            </th>
                     
                            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 d-none d-md-table-cell">
                                Date d'intégation
                            </th>
                            <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                                Action
                            </th>
                        </tr>
                    </thead>
                    <tbody id='conteneur-elmt'>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
</div>
</div>
`;

    const team = document.getElementById("teams");
    team.addEventListener("click", function (event) {
        event.preventDefault();
        page.innerHTML = show;
        const conteneur = document.getElementById("conteneur-elmt");
        // ID de l'élément à récupérer

        const elementId = team.getAttribute("data-id"); // Remplacez par l'ID souhaité

        // Construire l'URL de l'API Laravel
        const apiUrl = `/groupes/load-users/${elementId}`;

        // Effectuer la requête GET avec fetch
        fetch(apiUrl)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Erreur lors de la requête GET");
                }
                return response.json();
            })
            .then((data) => {
                // Traiter et afficher les données

                for (const user of data.users) {
                    let profilePhotoPath =
                        window.assetBaseUrl + "/" + user.profile;
                    let ligneAction = ` <a href="javascript:;" class="mx-3 deleteBtn" data-bs-toggle="tooltip" data-bs-original-title="retirer l'utilisateur"  data-id="${user.id}" data-action="supprimer">
                        <span>
                            <i class="cursor-pointer fas fa-trash text-secondary"></i>
                        </span>
                        </a>
                        
                    </td>
                </tr>`;
                
                    if (user.id == window.authUserId || user.id === 1) {
                        ligneAction = `                         
                    </td>
                </tr>`;
                    }
                    let ligne = `
                    <tr id="${user.id}" >
                    <td>
                        <div class="d-flex px-2 py-1">
                            <div>
                                <img src="${profilePhotoPath}"
                                class="avatar avatar-sm me-3" >
                            </div>
                            <div class="d-flex flex-column justify-content-center">
                                <h6 class="mb-0 text-sm">${user.name} ${user.firstname}</h6>
                                <p class="text-xs text-secondary mb-0">${user.pole.nom}</p>
                            </div>
                        </div>
                    </td>
                    <td class="text-center d-none d-md-table-cell">
                        <p class="text-xs font-weight-bold mb-0">${user.phone}</p>
                    </td>
                    <td class="text-center d-none d-md-table-cell">
                        <p class="text-xs font-weight-bold mb-0"> ${user.dateIntegration}</p>
                    </td>
                
                    <td class="text-center">
                        <a href="/membres/edit/${user.id}" class="mx-3" data-bs-toggle="tooltip" data-bs-original-title="Edit user">
                            <i class="fas fa-user-edit text-secondary"></i>
                        </a>
                      
                   `;
                    ligne += ligneAction;
                    conteneur.innerHTML += ligne;
                    conteneur.addEventListener("click", function (event) {
                        const link = event.target.closest(
                            'a[data-action="supprimer"]'
                        );
                        if (link) {
                            const id = link.getAttribute("data-id");
                            supprimer(id);
                        }
                    });
                }
            })
            .catch((error) => {
                console.error("Une erreur s'est produite :", error);
            });
    });
    function supprimer(itemId) {
        // Affiche une alerte de confirmation
        Swal.fire({
            title: "Êtes-vous sûr?",
            text: "Cette action ne peut pas être annulée.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Oui, supprimer!",
            cancelButtonText: "Annuler",
        }).then((result) => {
            if (result.isConfirmed) {
                // Envoie la requête DELETE via Axios à l'API pour supprimer l'élément
                axios
                    .delete("/api/groupes/membre-remove/" + itemId)
                    .then((response) => {
                        if (response.data.ok) {
                            // Supprime l'élément de la page et affiche une confirmation
                            document.getElementById(itemId).remove();
                            Swal.fire(
                                "Terminé!",
                                response.data.message,
                                "success"
                            );
                        } else {
                            // Affiche une modal d'erreur si la suppression a échoué
                            Swal.fire("Erreur!", response.data.error, "error");
                        }
                    })
                    .catch((error) => {
                        // Gère les erreurs liées à la requête (connexion, serveur, etc.)
                        console.error("Erreur :", error);
                    });
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                // Si l'utilisateur annule, affiche une alerte d'annulation
                Swal.fire("Annulé", "L'élément n'a pas été supprimé.", "info");
            }
        });
    }

    document
        .getElementById("overview")
        .addEventListener("click", function (event) {
            event.preventDefault();
            page.innerHTML = hot;
        });

    // Attache la fonction telecharger à chaque lien
});
