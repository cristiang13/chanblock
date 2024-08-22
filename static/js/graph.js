// Convertir la variable de Django a una variable JavaScript
let currentPage = 1;
let itemsPerPage = 10;
let selections = {};



function renderCheckboxes() {
    const container = document.getElementById('checkbox-container');
    container.innerHTML = ''; // Limpiar el contenedor

    let pageContent = variable_coinmetrics.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);
    pageContent.forEach(metric => {
        const isChecked = selections[metric[0]] ? 'checked' : '';
        container.innerHTML += `
            <div class="form-check">
                <input class="form-check-input" type="checkbox" value="${metric[0]}" id="${metric[0]}" ${isChecked} onchange="handleCheckboxChange(this)">
                <label class="form-check-label" for="${metric[0]}">
                    ${metric[1]} 
                </label>
            </div>`;
    });
}

function handleCheckboxChange(checkbox) {
    const metricId = checkbox.value;
    if (checkbox.checked) {
        selections[metricId] = true;
    } else {
        delete selections[metricId];
    }
}
function changePage(page) {
    currentPage = page;
    renderCheckboxes();
    renderPagination();
}


function renderPagination() {
    const pagination = document.getElementById('pagination');
    const totalPages = Math.ceil(variable_coinmetrics.length / itemsPerPage);
    const maxPagesToShow = 5; // Máximo de botones de página a mostrar alrededor de la página actual
    let startPage = Math.max(currentPage - Math.floor(maxPagesToShow / 2), 1);
    let endPage = Math.min(startPage + maxPagesToShow - 1, totalPages);

    pagination.innerHTML = '';
    pagination.className = 'pagination-container';

    // Botón "Primera página" y "Anterior"
    pagination.innerHTML += `<button class="pagination-button" onclick="changePage(1)" ${currentPage === 1 ? 'disabled' : ''}>&#171;&#171;</button>`;
    pagination.innerHTML += `<button class="pagination-button" onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>&#171;</button>`;

    // Números de página
    for (let i = startPage; i <= endPage; i++) {
        pagination.innerHTML += `<button class="${currentPage === i ? 'pagination-button active' : 'pagination-button'}" onclick="changePage(${i})">${i}</button>`;
    }

    // Botón "Siguiente" y "Última página"
    pagination.innerHTML += `<button class="pagination-button" onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>&#187;</button>`;
    pagination.innerHTML += `<button class="pagination-button" onclick="changePage(${totalPages})" ${currentPage === totalPages ? 'disabled' : ''}>&#187;&#187;</button>`;
}

function getSelectedValues() {
    let keys = Object.keys(selections);
    document.getElementById('spinner').style.display = 'inline-block'; // o 'block'
    document.getElementById('applyButton').disabled = true;
    // Utiliza Fetch para enviar los datos
    fetch('plot_metrics/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Obtener el token CSRF de Django
        },
        body: JSON.stringify({metrics: keys})
    })
    .then(response => response.json())
    .then(data => {
        // Actualiza el coin metrics
        const coin = document.querySelector('#title-coin');
        coin.innerHTML = data.metrics;

        // Actualiza el div con el nuevo gráfico
        const graphDiv = document.querySelector('.graph-section');
        graphDiv.innerHTML = data.plot;

        // Encuentra y evalúa todos los scripts dentro del div actualizado
        Array.from(graphDiv.querySelectorAll('script')).forEach(oldScript => {
            const newScript = document.createElement('script');
            Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });

           // Ocultar el spinner y habilitar el botón
           document.getElementById('spinner').style.display = 'none';
           document.getElementById('applyButton').disabled = false;
           deletSelectedValues();
           // Cerrar el modal si la operación fue exitosa
           $('#exampleModal').modal('hide');



    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


function deletSelectedValues() {
    selections = {};
    renderCheckboxes();
    renderPagination();

}

function cancelApply(){
    selections = {};
    renderCheckboxes();
}

// Función para obtener el cookie CSRF de Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function filterMetrics(category, page = 1) {
    let filteredMetrics;
    if (category === 'Adr-all') {
        // Filtra métricas que comienzan con 'Adr'
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('Adr'));
    }else if (category ==='Availability-all'){
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('AssetEOD'));
    }else if(category ==='Economics-all'){
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('Rev'));
    }else if(category ==='Fees-all'){
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('Fee'));
    }else if(category ==='Market-all'){
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('Cap') || metric[0].startsWith('ROI') || metric[0].startsWith('ReferenceRate') );
    }else if(category ==='Mining-all'){
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('DiffLast') || metric[0].startsWith('DiffMean') || metric[0].startsWith('HashRate') || metric[0].startsWith('Flow'));
    }else if(category ==='Supply-all'){
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('Sply'));
    }else if(category ==='Network-all'){
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('Blk'));
    }else if(category ==='Txn-all'){
        filteredMetrics = variable_coinmetrics.filter(metric => 
            metric[0].startsWith('TxT'));
    }else if(category ==='all'){
        renderCheckboxes();
        renderPagination();


    }

    // Implementar la paginación
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedMetrics = filteredMetrics.slice(start, end);

    // Actualiza la visualización de las métricas
    renderMetrics(paginatedMetrics);

    // Actualizar la paginación
    renderPaginationMenuFilter(filteredMetrics.length, page,category);
}



function renderPaginationMenuFilter(totalItems, currentPage,category) {
    const pagination = document.getElementById('pagination');
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const maxPagesToShow = 5; // Máximo de botones de página a mostrar alrededor de la página actual
    let startPage = Math.max(currentPage - Math.floor(maxPagesToShow / 2), 1);
    let endPage = Math.min(startPage + maxPagesToShow - 1, totalPages);

    pagination.innerHTML = '';
    pagination.className = 'pagination-container';

    // Botón "Primera página" y "Anterior"
    pagination.innerHTML += `<button class="pagination-button" onclick="filterMetrics('${category}', 1)" ${currentPage === 1 ? 'disabled' : ''}>&#171;&#171;</button>`;
    pagination.innerHTML += `<button class="pagination-button" onclick="filterMetrics('${category}', ${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>&#171;</button>`;

    // Números de página
    for (let i = startPage; i <= endPage; i++) {
        pagination.innerHTML += `<button class="${currentPage === i ? 'pagination-button active' : 'pagination-button'}" onclick="filterMetrics('${category}', ${i})">${i}</button>`;
    }

    // Botón "Siguiente" y "Última página"
    pagination.innerHTML += `<button class="pagination-button" onclick="filterMetrics('${category}', ${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>&#187;</button>`;
    pagination.innerHTML += `<button class="pagination-button" onclick="filterMetrics('${category}', ${totalPages})" ${currentPage === totalPages ? 'disabled' : ''}>&#187;&#187;</button>`;
}

function renderMetrics(metrics) {
    const container = document.getElementById('checkbox-container');
    container.innerHTML = ''; // Limpiar el contenedor
    metrics.forEach(metric => {
        const isChecked = selections[metric[0]] ? 'checked' : '';
        container.innerHTML += `
            <div class="form-check">
                <input class="form-check-input" type="checkbox" value="${metric[0]}" id="${metric[0]}" ${isChecked} onchange="handleCheckboxChange(this)">
                <label class="form-check-label" for="${metric[0]}">
                    ${metric[1]}
                </label>
            </div>`;
    });
}

// Inicializar la primera renderización
renderCheckboxes();
renderPagination();
// renderPaginationMenuFilter();
