async function getUserData() {
    const response = await fetch('/users');
    return response.json();
}

function loadTable(users) {
    console.log(users)
    const table = document.querySelector('#result');
    for (let user of users) {
        table.innerHTML += `<tr>
            <td>${user.id}</td>
            <td>${user.email}</td>
        </tr>`;
    }
}

async function main() {
    const users = await getUserData();
    loadTable(users);
}

main();