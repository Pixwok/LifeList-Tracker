import { fetchJSON } from "./api.js";
import { createElement } from "./dom.js";
import { openModalForm, closeModal } from "./form.js";

// Récupère l'ID de l'objectif dans URL
const urlParam = new URLSearchParams(window.location.search);
const goal_id = urlParam.get('id');

if (goal_id) {
    try {
        const responseGoal = await fetchJSON(`/goals/${goal_id}`);
        const dataGoal = responseGoal.data

        document.querySelector('#goal-name').innerHTML = dataGoal.name;

        // Goal info
        const goalInfoContainer =  document.querySelector('#goal-info');
        const category = await fetchJSON(`/categories/${dataGoal.categorie_id}`);

        // Création des elements goal-info
        const categoryTag = createElement('span', {class: 'tag'})
        categoryTag.innerText = category.data.name;
        const avancement = createElement('span');
        avancement.innerText = "Avancement: " + dataGoal.advancement + "%";
        const deadline = createElement('span');
        deadline.innerText = "Deadline: " + new Date(dataGoal.deadline).toLocaleDateString('fr');

        goalInfoContainer.append(categoryTag);
        goalInfoContainer.append(avancement);
        goalInfoContainer.append(deadline);

        // Gestion des tâches
        const taskListContainer = document.querySelector('#task-list');
        const tasks = await fetchJSON(`/goals/${goal_id}/task`);

        displayTask(tasks.data);

        //Création d'une tâche
        document.querySelector('#create-task').addEventListener("click", () => {
            openModalForm('modal-edit-task')
        })

        // Edition d'un tâche
        const editTaskForm = document.querySelector('#form-edit-task');
        editTaskForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const task_id = editTaskForm.getAttribute('data-id');
            if (task_id) {
                const request = await fetchJSON(`/task/${task_id}`, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        "name": editTaskForm.elements.name.value,
                        "description": editTaskForm.elements.description.value,
                        "deadline": editTaskForm.elements.deadline.value
                    })
                });
            } else {
                const request = await fetchJSON(`/task`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        "name": editTaskForm.elements.name.value,
                        "description": editTaskForm.elements.description.value,
                        "deadline": editTaskForm.elements.deadline.value,
                        "objectif_id": goal_id
                    })
                });
            }
            closeModal('modal-edit-task');
            editTaskForm.reset();

            const tasks = await fetchJSON(`/goals/${goal_id}/task`);
            displayTask(tasks.data);
        })

        document.querySelector('#modal-edit-task').addEventListener('click', (event) => {
            // Vérifie si l'on clique en dehors du formaulaire
            if (event.target.classList.contains('modal-overlay') && event.target.classList.contains('open')) {
            closeModal(event.target.id);
            }
        });

        // Edit objectif
        document.querySelector('#edit-goal').addEventListener("click", async () => {
            openModalForm('modal-edit-goal')
            document.querySelector('#goal-name').value = dataGoal.name;
            document.querySelector('#goal-deadline').value = dataGoal.deadline;
            const categorie = await fetchJSON('/categories/');
            const selectForm = document.querySelector('#goal-categorie');
            categorie.data.forEach(element => {
                const optionForm = createElement('option', {value: element.id});
                optionForm.innerText = element.name;
                selectForm.append(optionForm);
            });
            console.log(dataGoal);
        });

        const formCreateGoal= document.querySelector('#form-edit-goal')
            formCreateGoal.addEventListener('submit', async (event) => {
            event.preventDefault();
            const response = await fetchJSON(`/goals/${goal_id}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    "name": formCreateGoal.elements.name.value,
                    "deadline": formCreateGoal.elements.deadline.value,
                    "categorie_id": formCreateGoal.elements.categorie.value
                })
            });
            closeModal('modal-edit-goal');
        });

        document.querySelector('#modal-edit-goal').addEventListener('click', (event) => {
            // Vérifie si l'on clique en dehors du formaulaire
            if (event.target.classList.contains('modal-overlay') && event.target.classList.contains('open')) {
            closeModal(event.target.id);
            }
        });

        // Suppression objectif
        document.querySelector('#delete-goal').addEventListener("click", () => {
            deleteGoal(goal_id);
        });


    } catch (error) {
        window.location.href = '/'; //Redirection
        console.log(error);
    }
} else {
    window.location.href = '/'; //Redirection 
}

function displayTask(tasks) {
    const todoContainer = document.querySelector('#taskTodo-List');
    const completeContainer = document.querySelector('#taskComplete-List');

    todoContainer.innerHTML = "";
    completeContainer.innerHTML = "";

    const tasksTodo = tasks.filter((task) => task.statut == false);
    const tasksComplete = tasks.filter((task) => task.statut == true);
    
    // Tâches en cours
    tasksTodo.forEach(task => {
        const li = createElement('li', {class: 'task'});
        const deadlineFormat = new Date(task.deadline);
        li.innerHTML = `
            <div class="task-left">
            <input type="checkbox" data-id="${task.id}" ${task.statut ? 'checked' : ''}>
            <div class="task-content">
            <h4>${task.name}</h4>
            ${task.description ? `<p>${task.description}</p>` : ''}
            </div>
            </div>
            <span class="task-deadline">${deadlineFormat.toLocaleDateString("fr")}</span>
        `;
        todoContainer.appendChild(li);

        // Ajoute un écouteur pour cocher/décocher
        li.querySelector('input[type="checkbox"]').addEventListener('change', () => toggleTaskComplete(task.id, li));

        // Ajoute un écouteur pour éditer la tâche
        li.addEventListener('click', (e) => {
            if (e.target.type !== 'checkbox') {
                editTask(task);
            }
        });
    });

    // Tâches terminé
    tasksComplete.forEach(task => {
        const li = createElement('li', {class: 'task'});
        const deadlineFormat = new Date(task.deadline);
        li.innerHTML = `
            <div class="task-left">
            <input type="checkbox" data-id="${task.id}" ${task.statut ? 'checked' : ''}>
            <div class="task-content">
            <h4>${task.name}</h4>
            ${task.description ? `<p>${task.description}</p>` : ''}
            </div>
            </div>
            <span class="task-deadline">${deadlineFormat.toLocaleDateString("fr")}</span>
        `;
        completeContainer.appendChild(li);

        // Ajoute un écouteur pour cocher/décocher
        li.querySelector('input[type="checkbox"]').addEventListener('change', () => toggleTaskComplete(task.id, li));
    });
}

async function toggleTaskComplete(taskId, liElement) {
  const isChecked = liElement.querySelector('input[type="checkbox"]').checked;

  try {
    // Met à jour la tâche via l'API
    await fetch(`/task/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ statut: isChecked }),
    });

    // Recharge les tâches pour mettre à jour l'affichage
    const tasks = await fetchJSON(`/goals/${goal_id}/task`);
    displayTask(tasks.data);
  } catch (error) {
    console.error("Erreur lors de la mise à jour de la tâche :", error);
  }
}

async function editTask(task) {
    openModalForm('modal-edit-task');
    document.querySelector('#task-name').value = task.name;
    document.querySelector('#task-desc').value = task.description;
    document.querySelector('#task-deadline').value = task.deadline;

    //Stockage Id task dans form
    document.querySelector('#form-edit-task').setAttribute('data-id', task.id);
}

function deleteGoal(goalId) {
    const modalGoalId = document.querySelector('#goal-id');
    modalGoalId.innerText = goalId;
    openModalForm('modal-delete-goal');


    document.querySelector('#modal-delete-goal').addEventListener('click', (event) => {
        // Vérifie si l'on clique en dehors du formaulaire
        if (event.target.classList.contains('modal-overlay') && event.target.classList.contains('open')) {
        closeModal(event.target.id);
        }
    });

    document.querySelector('#cancel-delete').addEventListener('click', () => {
        closeModal('modal-delete-goal');
    });

    document.querySelector('#confirm-delete').addEventListener('click', async () => {
        //Suppression des tâches associé
        const taskForGoal = await fetchJSON(`/goals/${goal_id}/task`);
        for (const task of taskForGoal.data) {
            const deleteRequest = await fetchJSON(`/task/${task.id}`, {
                method: 'DELETE'
            });
        }
        //Suppression objectif
        const deleteRequest = await fetchJSON(`/goals/${goal_id}`, {
            method: 'DELETE'
        });

        if (deleteRequest.success) {
            window.location.href = '/';
        }
    });
}