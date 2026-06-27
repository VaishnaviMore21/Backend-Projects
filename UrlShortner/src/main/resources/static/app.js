const form = document.getElementById('shorten-form');
const urlInput = document.getElementById('fullUrl');
const submitButton = document.getElementById('submit-button');
const feedback = document.getElementById('feedback');
const resultCard = document.getElementById('result-card');
const shortUrlOutput = document.getElementById('short-url-output');
const copyButton = document.getElementById('copy-button');
const openLink = document.getElementById('open-link');
const targetLink = document.getElementById('target-link');

function showFeedback(message, type) {
    feedback.textContent = message;
    feedback.className = `feedback ${type}`;
}

function hideFeedback() {
    feedback.textContent = '';
    feedback.className = 'feedback hidden';
}

function showResult(shortUrl, originalUrl) {
    shortUrlOutput.value = shortUrl;
    openLink.href = shortUrl;
    targetLink.href = originalUrl;
    targetLink.textContent = 'Open original URL';
    resultCard.classList.remove('hidden');
}

function hideResult() {
    shortUrlOutput.value = '';
    openLink.href = '#';
    targetLink.href = '#';
    resultCard.classList.add('hidden');
}

async function shortenUrl(event) {
    event.preventDefault();
    hideFeedback();
    hideResult();

    const fullUrl = urlInput.value.trim();
    if (!fullUrl) {
        showFeedback('Please enter a URL to shorten.', 'error');
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = 'Shortening...';

    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ fullUrl })
        });

        const responseBody = await response.json().catch(() => ({}));
        if (!response.ok) {
            const errorMessage = responseBody.error || 'Failed to shorten the URL.';
            showFeedback(errorMessage, 'error');
            return;
        }

        showFeedback('Short URL created successfully.', 'success');
        showResult(responseBody.shortUrl, fullUrl);
    } catch (error) {
        showFeedback('Unable to reach the API. Please try again.', 'error');
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Shorten';
    }
}

async function copyShortUrl() {
    if (!shortUrlOutput.value) {
        return;
    }

    try {
        await navigator.clipboard.writeText(shortUrlOutput.value);
        showFeedback('Short URL copied to clipboard.', 'success');
    } catch (error) {
        shortUrlOutput.select();
        document.execCommand('copy');
        showFeedback('Short URL copied to clipboard.', 'success');
    }
}

form.addEventListener('submit', shortenUrl);
copyButton.addEventListener('click', copyShortUrl);

