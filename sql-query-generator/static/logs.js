// Logs page script
const API_BASE = '/api';
let logsPage = 1;
const logsPageSize = 10;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadLogs();
    loadStats();
});

// Load and display logs
async function loadLogs() {
    try {
        const response = await fetch(`${API_BASE}/logs?page=${logsPage}&page_size=${logsPageSize}`);
        
        if (!response.ok) {
            throw new Error('Failed to load logs');
        }

        const data = await response.json();
        displayLogs(data.logs || []);
        updateLogsPagination(data.total);
    } catch (error) {
        console.error('Error loading logs:', error);
        showLogsError(error.message);
    }
}

// Display logs in table
function displayLogs(logs) {
    const tbody = document.getElementById('logsTableBody');
    
    if (!logs || logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No logs found</td></tr>';
        return;
    }

    tbody.innerHTML = logs.map(log => `
        <tr>
            <td>${new Date(log.created_at).toLocaleString()}</td>
            <td>${escapeHtml(log.user_email || 'anonymous')}</td>
            <td><span title="${escapeHtml(log.question)}">${escapeHtml(truncate(log.question, 50))}</span></td>
            <td>
                <span class="status-badge status-${log.execution_status}">
                    ${log.execution_status}
                </span>
            </td>
            <td>${log.rows_returned || 0}</td>
            <td>${log.execution_time_ms || '-'}</td>
            <td><span title="${escapeHtml(log.error_message || '-')}">${escapeHtml(truncate(log.error_message || '-', 30))}</span></td>
        </tr>
    `).join('');
}

// Load and display statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/logs/stats?hours=24`);
        
        if (!response.ok) {
            throw new Error('Failed to load stats');
        }

        const data = await response.json();
        displayStats(data.stats || {});
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Display statistics
function displayStats(stats) {
    const statsSection = document.getElementById('statsSection');
    
    if (Object.keys(stats).length === 0) {
        statsSection.style.display = 'none';
        return;
    }

    document.getElementById('statTotalQueries').textContent = stats.total_queries || 0;
    document.getElementById('statSuccessful').textContent = stats.successful_queries || 0;
    document.getElementById('statFailed').textContent = stats.failed_queries || 0;
    document.getElementById('statAvgTime').textContent = 
        Math.round(stats.avg_execution_time || 0) + 'ms';
    
    statsSection.style.display = 'grid';
}

// Update pagination controls
function updateLogsPagination(total) {
    const totalPages = Math.ceil(total / logsPageSize);
    document.getElementById('logsPageInfo').textContent = 
        `Page ${logsPage} of ${totalPages}`;
    
    document.getElementById('prevLogsBtn').disabled = logsPage === 1;
    document.getElementById('nextLogsBtn').disabled = logsPage === totalPages;
}

// Pagination handlers
document.getElementById('prevLogsBtn').addEventListener('click', () => {
    if (logsPage > 1) {
        logsPage--;
        loadLogs();
        window.scrollTo(0, 0);
    }
});

document.getElementById('nextLogsBtn').addEventListener('click', () => {
    logsPage++;
    loadLogs();
    window.scrollTo(0, 0);
});

// Utility functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function truncate(text, maxLength) {
    if (!text) return '-';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

function showLogsError(message) {
    const tbody = document.getElementById('logsTableBody');
    tbody.innerHTML = `<tr><td colspan="7" class="text-center error-message">${escapeHtml(message)}</td></tr>`;
}
