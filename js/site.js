
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.faq-item .faq-question').forEach((q) => {
    q.addEventListener('click', () => q.parentElement.classList.toggle('active'));
  });
});
