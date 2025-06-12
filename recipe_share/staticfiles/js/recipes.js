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
          const li = document.createElement("li");
          li.textContent = text;
          
          commentInput.value = "";
        }
      });
    });