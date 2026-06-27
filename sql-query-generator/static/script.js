// API base URL
const API_BASE = '/api';

// Current pagination state
let currentPage = 1;
let currentPageSize = 20;
let currentQuestion = '';
let currentResults = null;
let currentSql = '';

// DOM elements
const queryForm = document.getElementById('queryForm');
const questionField = document.getElementById('question');
const previewBtn = document.getElementById('previewBtn');
const executeBtn = document.getElementById('executeBtn');
const explainQueryCheckbox = document.getElementById('explainQuery');
const loadingState = document.getElementById('loadingState');
const sqlSection = document.getElementById('sqlSection');
const sqlCode = document.getElementById('sqlCode');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const copySqlBtn = document.getElementById('copySqlBtn');
const explainBtn = document.getElementById('explainBtn');
const explanation = document.getElementById('explanation');

// Example link handlers
document.querySelectorAll('.example').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        questionField.value = e.target.getAttribute('data-question');
    });
});

// Preview button
previewBtn.addEventListener('click', async () => {
    const question = questionField.value.trim();
    if (!question) {
        showError('Please enter a question');
        return;
    }

    try {
        showLoading(true);
        const response = await fetch(`${API_BASE}/query/preview`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-User-Email': 'user@example.com'
            },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Preview failed');
        }

        const data = await response.json();
        currentSql = data.query;
        
        displaySql(data.query, data.confidence);
        displayPreviewResults(data.preview || []);
        showLoading(false);
    } catch (error) {
        showError(error.message);
        showLoading(false);
    }
});

// Query form submission
queryForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const question = questionField.value.trim();
    if (!question) {
        showError('Please enter a question');
        return;
    }

    try {
        showLoading(true);
        currentQuestion = question;
        currentPage = 1;

        const response = await fetch(`${API_BASE}/query/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-User-Email': 'user@example.com'
            },
            body: JSON.stringify({
                question: question,
                page: 1,
                page_size: currentPageSize,
                explain_query: explainQueryCheckbox.checked
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Query execution failed');
        }

        const data = await response.json();
        
        currentSql = data.query;
        currentResults = data;
        
        displaySql(data.query, data.confidence);
        displayResults(data.results, data.total_rows, data.page, data.page_size, data.execution_time_ms);
        showLoading(false);
    } catch (error) {
        showError(error.message);
        showLoading(false);
    }
});

// Copy SQL button
copySqlBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(currentSql).then(() => {
        const originalText = copySqlBtn.textContent;
        copySqlBtn.textContent = '✓ Copied!';
        setTimeout(() => {
            copySqlBtn.textContent = originalText;
        }, 2000);
    });
});

// Explain button
explainBtn.addEventListener('click', async () => {
    if (!currentSql) return;

    try {
        explainBtn.disabled = true;
        explainBtn.textContent = 'Generating explanation...';

        const response = await fetch(`${API_BASE}/query/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: currentQuestion,
                explain: true
            })
        });

        if (!response.ok) throw new Error('Failed to generate explanation');

        const data = await response.json();
        
        explanation.textContent = data.explanation || 'No explanation available';
        explanation.style.display = 'block';
        explainBtn.textContent = 'Explanation Generated ✓';
    } catch (error) {
        showError(error.message);
    } finally {
        explainBtn.disabled = false;
    }
});

// Pagination buttons
document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        executeQueryForPage();
    }
});

document.getElementById('nextBtn').addEventListener('click', () => {
    if (currentResults && currentPage * currentPageSize < currentResults.total_rows) {
        currentPage++;
        executeQueryForPage();
    }
});

async function executeQueryForPage() {
    try {
        showLoading(true);

        const response = await fetch(`${API_BASE}/query/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-User-Email': 'user@example.com'
            },
            body: JSON.stringify({
                question: currentQuestion,
                page: currentPage,
                page_size: currentPageSize
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Query execution failed');
        }

        const data = await response.json();
        currentResults = data;
        
        displayResults(data.results, data.total_rows, data.page, data.page_size, data.execution_time_ms);
        showLoading(false);
    } catch (error) {
        showError(error.message);
        showLoading(false);
    }
}

// Display functions
function displaySql(sql, confidence) {
    sqlCode.textContent = sql;
    sqlSection.style.display = 'block';
    explanation.style.display = 'none';
    explainBtn.textContent = 'Explain';
}

function displayPreviewResults(results) {
    if (!results || results.length === 0) {
        displayResults([], 0, 1, currentPageSize, 0);
        return;
    }

    const columns = Object.keys(results[0]);
    
    // Build table header
    const thead = document.getElementById('tableHead');
    thead.innerHTML = `<tr>${columns.map(col => `<th>${escapeHtml(col)}</th>`).join('')}</tr>`;
    
    // Build table body with preview rows
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = results.map(row => 
        `<tr>${columns.map(col => `<td>${formatValue(row[col])}</td>`).join('')}</tr>`
    ).join('');
    
    resultsSection.style.display = 'block';
    document.getElementById('paginationSection').style.display = 'none';
    document.getElementById('resultsMeta').textContent = `Preview (${results.length} rows)`;
}

function displayResults(results, totalRows, page, pageSize, executionTime) {
    if (!results || results.length === 0) {
        document.getElementById('tableHead').innerHTML = '';
        document.getElementById('tableBody').innerHTML = '<tr><td colspan="10" class="text-center">No results found</td></tr>';
        resultsSection.style.display = 'block';
        document.getElementById('paginationSection').style.display = 'none';
        document.getElementById('resultsMeta').textContent = 'No results';
        return;
    }

    const columns = Object.keys(results[0]);
    
    // Build table header
    const thead = document.getElementById('tableHead');
    thead.innerHTML = `<tr>${columns.map(col => `<th>${escapeHtml(col)}</th>`).join('')}</tr>`;
    
    // Build table body
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = results.map(row => 
        `<tr>${columns.map(col => `<td>${formatValue(row[col])}</td>`).join('')}</tr>`
    ).join('');
    
    // Update metadata
    const start = (page - 1) * pageSize + 1;
    const end = Math.min(start + results.length - 1, totalRows);
    document.getElementById('resultsMeta').textContent = 
        `Showing ${start}-${end} of ${totalRows} rows | Execution time: ${executionTime}ms`;
    
    // Update pagination
    const totalPages = Math.ceil(totalRows / pageSize);
    document.getElementById('pageInfo').textContent = `Page ${page} of ${totalPages}`;
    document.getElementById('prevBtn').disabled = page === 1;
    document.getElementById('nextBtn').disabled = page === totalPages;
    
    resultsSection.style.display = 'block';
    document.getElementById('paginationSection').style.display = 'flex';
    errorMessage.style.display = 'none';
}

function showLoading(show) {
    loadingState.style.display = show ? 'block' : 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    resultsSection.style.display = 'none';
}

function formatValue(value) {
    if (value === null || value === undefined) {
        return '<span style="color: #9ca3af;">NULL</span>';
    }
    if (typeof value === 'boolean') {
        return value ? '✓' : '✗';
    }
    if (typeof value === 'number') {
        return new Intl.NumberFormat().format(value);
    }
    return escapeHtml(String(value));
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
