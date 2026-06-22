import { fetchJSON } from "./api.js";
import { createElement } from "./dom.js";

/*Dashboard objectifs*/
async function Dashboard() {
    const responseGoals = await fetchJSON("/goals");
    const dataGoals = responseGoals.data

    const responseTasks = await fetchJSON("/task");
    const dataTasks = responseTasks.data

    // Objectifs en cours
    const activeGoal = dataGoals.filter((goal) => goal.statut == false);
    // Objectifs terminés
    const completeGoal = dataGoals.filter((goal) => goal.statut == true);
    // Tâches à faire
    const taskTodo = dataTasks.filter((task) => task.statut == false);
    // Echéance à venir
    const deadline = dataGoals.toSorted(dataGoals.deadline)[0].deadline;
    const deadlineFormat = new Date(deadline);
    const nextDeadline = Math.ceil((deadlineFormat.getTime() - Date.now()) / 86400000 )
    // Objectifs en retard
    const lateGoal = dataGoals.filter((goal) => new Date(goal.deadline) < Date.now()).filter((goal) => goal.statut == false);
    //Card KPI
    document.getElementById('activeGoals').innerHTML = activeGoal.length;
    document.getElementById('goalsComplete').innerHTML = completeGoal.length;
    document.getElementById('taskTodo').innerHTML = taskTodo.length;
    document.getElementById('nextDeadLine').innerHTML = nextDeadline + " J";
    document.getElementById('lateGoal').innerHTML = lateGoal.length;

    //Card Goal
    const GoalContainer = document.getElementById('goals-list');
    GoalContainer.innerHTML = "";

    for (const element of activeGoal) {
        const linkCard = createElement('a', {href: '/', class: 'card-link'});
        const card = createElement('div', {class: 'card'});
        const cardHeader = createElement('div', {class: 'card-header'});
        const spanCategory = createElement('span', {class: 'tag'});
        const categorie = await fetchJSON(`/categories/${element.categorie_id}`);
        spanCategory.innerText = categorie.data.name;
        const spanDeadline = createElement('span');
        spanDeadline.innerText = element.deadline;
        const cardBody = createElement('div', {class: 'card-body'})
        const h4 = createElement('h4');
        h4.innerText = element.name;
        const progress = createElement('progress', {class: 'progressBar', max: 100, value: element.advancement});
        const cardFooter = createElement('div', {class: 'card-footer'});
        const spanAvancement = createElement('span');
        spanAvancement.innerText = element.advancement + "%";
        const tasks = await fetchJSON(`/goals/${element.id}/task`);
        const spanTask = createElement('span');
        spanTask.innerText = tasks.data.filter((task) => task.statut == true).length + "/" + tasks.data.length + " tâches";

        GoalContainer.append(linkCard);
        linkCard.append(card);
        card.append(cardHeader);
        cardHeader.append(spanCategory);
        cardHeader.append(spanDeadline);
        card.append(cardBody);
        cardBody.append(h4);
        cardBody.append(progress);
        card.append(cardFooter);
        cardFooter.append(spanAvancement)
        cardFooter.append(spanTask);
    }
}

Dashboard();