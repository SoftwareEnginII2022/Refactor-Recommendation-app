async function getRequestData() {
    const response = await fetch('/requests');
    return response.json();
}

function loadTable(requests) {
    console.log(requests)
    const table = document.querySelector('#result');
    for (let request of requests) {
        table.innerHTML += `<tr>
            <td>${request.reqID}</td>
            <td>${request.staffID}</td>
            <td>${request.studentID}</td>
            <td>${request.deadline}</td>
            <td>${request.requestBody}</td>
            <td>${request.status}</td>
        </tr>`;
    }
}

async function main() {
    const requests = await getRequestData();
    loadTable(requests);
}

main();