import { fetchJSON } from "./api.js";
import { createElement } from "./dom.js";

/*Dashboard objectifs*/
async function Dashboard() {
    const response = await fetchJSON("/goals");
    const data = response.data

    // Objectifs en cours
    const activeGoal = data.filter((goal) => goal.statut == false);
    // Objectifs terminés
    const completeGoal = data.filter((goal) => goal.statut == true);
    // Echéance à venir
    const deadline = data.toSorted(data.deadline)[0].deadline;
    const deadlineFormat = new Date(deadline);
    const nextDeadline = Math.ceil((deadlineFormat.getTime() - Date.now()) / 86400000 )
    // Objectifs en retard
    const lateGoal = data.filter((goal) => new Date(goal.deadline) < Date.now()).filter((goal) => goal.statut == false);
    //Card KPI
    document.getElementById('activeGoals').innerHTML = activeGoal.length;
    document.getElementById('goalsComplete').innerHTML = completeGoal.length;
    document.getElementById('nextDeadLine').innerHTML = nextDeadline + " J";
    document.getElementById('lateGoal').innerHTML = lateGoal.length;

    //Card Goal
    const GoalContainer = document.getElementById('goals-list');
    GoalContainer.innerHTML = "";

    for (const element of activeGoal) {
        const card = createElement('div', {class: 'card'});
        const cardHeader = createElement('div', {class: 'card-header'});
        const spanCategory = createElement('span', {class: ''});
        const categorie = await fetchJSON(`/categories/${element.categorie_id}`);
        spanCategory.innerText = categorie.data.name;
        const spanDeadline = createElement('span');
        spanDeadline.innerText = element.deadline;
        const cardBody = createElement('div', {class: 'card-body'})
        const h3 = createElement('h3');
        h3.innerText = element.name;
        

        GoalContainer.append(card);
        card.append(cardHeader);
        cardHeader.append(spanCategory);
        cardHeader.append(spanDeadline);
        card.append(cardBody);
        cardBody.append(h3);
    }
}

Dashboard();