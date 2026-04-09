const API_BASE = "/api";

let currentJoke = null;

// DOM Elements
const categoriesScreen = document.getElementById("categories-screen");
const jokeScreen = document.getElementById("joke-screen");
const categoriesGrid = document.getElementById("categories");
const jokeText = document.getElementById("joke-text");
const jokeCategory = document.getElementById("joke-category");
const jokeRating = document.getElementById("joke-rating");
const jokeVotes = document.getElementById("joke-votes");
const backBtn = document.getElementById("back-btn");
const likeBtn = document.getElementById("like-btn");
const dislikeBtn = document.getElementById("dislike-btn");
const ratingMessage = document.getElementById("rating-message");

// Load categories
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories`);
        if (!response.ok) throw new Error("Failed to load categories");
        const categories = await response.json();

        categoriesGrid.innerHTML = "";
        for (const [key, label] of Object.entries(categories)) {
            const btn = document.createElement("button");
            btn.className = "category-btn";
            btn.textContent = label;
            btn.onclick = () => loadJoke(key);
            categoriesGrid.appendChild(btn);
        }
    } catch (error) {
        categoriesGrid.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    }
}

// Load a joke from category
async function loadJoke(category) {
    try {
        const response = await fetch(`${API_BASE}/joke/${category}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to load joke");
        }

        currentJoke = await response.json();
        displayJoke();
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Display joke on screen
function displayJoke() {
    if (!currentJoke) return;

    jokeText.textContent = currentJoke.text;
    jokeCategory.textContent = currentJoke.category;
    updateRatingDisplay(currentJoke.rating, currentJoke.votes);

    // Hide rating message
    ratingMessage.classList.add("hidden");

    // Enable buttons
    likeBtn.disabled = false;
    dislikeBtn.disabled = false;

    // Switch screens
    categoriesScreen.classList.add("hidden");
    jokeScreen.classList.remove("hidden");
}

// Update rating display
function updateRatingDisplay(rating, votes) {
    jokeRating.textContent = `⭐ ${rating}`;
    jokeVotes.textContent = votes > 0 ? `(${votes} votes)` : "(No ratings yet)";
}

// Rate joke
async function rateJoke(isLike) {
    if (!currentJoke) return;

    likeBtn.disabled = true;
    dislikeBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/rate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                joke_id: currentJoke.id,
                is_like: isLike,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to rate joke");
        }

        const result = await response.json();

        // Update display
        updateRatingDisplay(result.new_rating, result.new_votes);

        // Show message
        ratingMessage.textContent = `${result.message} Thanks for rating!`;
        ratingMessage.className = "rating-message success";

        // Return to menu after short delay
        setTimeout(() => {
            showCategories();
        }, 1500);
    } catch (error) {
        ratingMessage.textContent = `❌ Error: ${error.message}`;
        ratingMessage.className = "rating-message error";
        likeBtn.disabled = false;
        dislikeBtn.disabled = false;
    }
}

// Show categories screen
function showCategories() {
    currentJoke = null;
    jokeScreen.classList.add("hidden");
    categoriesScreen.classList.remove("hidden");
    ratingMessage.classList.add("hidden");
}

// Event listeners
backBtn.onclick = showCategories;
likeBtn.onclick = () => rateJoke(true);
dislikeBtn.onclick = () => rateJoke(false);

// Initialize
loadCategories();
