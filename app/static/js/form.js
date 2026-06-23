export function openModalForm(modalId) {
    const modalOverlay = document.getElementById(modalId);
    if (!modalOverlay) return;
    modalOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
}

export function closeModal(modalId) {
  const modalOverlay = document.getElementById(modalId);
  if (!modalOverlay) return;

  modalOverlay.classList.remove('open');
  document.body.style.overflow = '';
}

export function initForm() {
    document.querySelectorAll('.modal-overlay.open').forEach(overlay => {
        closeModal(overlay.id);
    });
}