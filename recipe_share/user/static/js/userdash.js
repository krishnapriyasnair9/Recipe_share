document.addEventListener("DOMContentLoaded", function () {
  const uploadBtn = document.getElementById("uploadBtn");
  const uploadModal = document.getElementById("uploadModal");
  const closeBtn = document.getElementById("closeUpload");

  // Show the modal
  uploadBtn.addEventListener("click", function () {
    uploadModal.style.display = "block";
  });

  // Close the modal
  closeBtn.addEventListener("click", function () {
    uploadModal.style.display = "none";
  });

  // Close modal when clicking outside the modal content
  window.addEventListener("click", function (e) {
    if (e.target === uploadModal) {
      uploadModal.style.display = "none";
    }
  });
});
const toggleBtn = document.getElementById('profileToggle');
  const sidebar = document.getElementById('profileSidebar');

  toggleBtn.addEventListener('click', (e) => {
    e.preventDefault();
    sidebar.classList.toggle('show');
  });

  // Optional: Hide when clicking outside
  document.addEventListener('click', (e) => {
    if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
      sidebar.classList.remove('show');
    }
  });
  const viewLink = document.getElementById('viewProfileLink');
  const modal = document.getElementById('profileModal');
  const closeBtn = document.getElementById('closeModal');

  viewLink.onclick = function (e) {
    e.preventDefault(); // prevent actual link
    modal.style.display = 'block';
  };

  closeBtn.onclick = function () {
    modal.style.display = 'none';
  };

  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  };