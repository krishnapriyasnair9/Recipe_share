document.addEventListener("DOMContentLoaded", () => {
      const modal = document.getElementById("recipeModal");
      const modalTitle = document.getElementById("modalTitle");
      const modalImage = document.getElementById("modalImage");
      const modalDescription = document.getElementById("modalDescription");
      const modalUploader = document.getElementById("modalUploader");
      const modalContact = document.getElementById("modalContact");
      const modalIngredients = document.getElementById("modalIngredients");
      
      const commentInput = document.getElementById("commentInput");

      document.querySelectorAll(".view-more-btn").forEach(button => {
        button.addEventListener("click", (e) => {
          const card = e.target.closest(".recipe-card");
          modalTitle.textContent = card.dataset.title;
          modalImage.src = card.dataset.image;
          modalDescription.textContent = card.dataset.description;
          modalUploader.textContent = card.dataset.uploader;
          modalContact.textContent = card.dataset.contact;
          modalIngredients.textContent = card.dataset.ingredients;
          modal.style.display = "block";
        });
      });

      document.querySelector(".close").onclick = () => modal.style.display = "none";
      window.onclick = e => { if (e.target == modal) modal.style.display = "none"; };

      document.getElementById("postCommentBtn").addEventListener("click", () => {
  const text = commentInput.value.trim();
  if (text) {
    const recipeTitle = modalTitle.textContent;

    fetch('/post-comment/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // CSRF token helper
      },
      body: JSON.stringify({
        text: text,
        title: recipeTitle
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert("Comment posted!");
        commentInput.value = '';
      } else {
        alert(data.message || "Error posting comment.");
      }
    });
  }
});

// CSRF helper
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

});
// Add this to your existing JavaScript or create a new file
document.addEventListener('DOMContentLoaded', () => {
  // ... your existing modal code ...

  // Live search functionality (optional)
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      const searchTerm = this.value.toLowerCase();
      const recipeCards = document.querySelectorAll('.recipe-card');
      
      recipeCards.forEach(card => {
        const title = card.dataset.title.toLowerCase();
        const description = card.dataset.description.toLowerCase();
        const ingredients = card.dataset.ingredients.toLowerCase();
        
        if (title.includes(searchTerm) || 
            description.includes(searchTerm) || 
            ingredients.includes(searchTerm)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
});