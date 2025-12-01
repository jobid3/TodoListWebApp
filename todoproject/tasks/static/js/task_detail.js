let deleteUrl = null;
let deleteSubtaskItem = null;

// Helper function for POST requests
async function postForm(url, formData, csrfToken) {
  formData.append('csrfmiddlewaretoken', csrfToken);
  const response = await fetch(url, {
    method: 'POST',
    body: formData
  });
  return response;
}

// Show save status
function showStatus(element, message, isError = false) {
  element.textContent = message;
  element.style.color = isError ? '#dc2626' : '#10b981';
  setTimeout(() => { element.textContent = ''; }, 2000);
}

// Initialize task detail page
function initTaskDetail(config) {
  const { csrfToken, subtaskCreateUrl, taskUpdateUrl } = config;

  // Save Task Changes
  document.getElementById('edit-task-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const statusEl = document.getElementById('save-status');
    
    try {
      const response = await postForm(taskUpdateUrl, formData, csrfToken);
      if (response.ok) {
        document.getElementById('task-title').textContent = formData.get('title');
        
        const descDisplay = document.getElementById('task-description-display');
        const desc = formData.get('description');
        descDisplay.innerHTML = desc.replace(/\n/g, '<br>');
        descDisplay.style.display = desc ? 'block' : 'none';
        
        const isCompleted = formData.has('is_completed');
        const statusBadge = document.getElementById('task-status');
        statusBadge.textContent = isCompleted ? 'Completed' : 'Open';
        statusBadge.className = 'status ' + (isCompleted ? 'completed' : 'open');
        
        showStatus(statusEl, '✓ Saved!');
      } else {
        showStatus(statusEl, '✗ Error saving', true);
      }
    } catch (error) {
      showStatus(statusEl, '✗ Error saving', true);
    }
  });

  // Add Subtask
  document.getElementById('add-subtask-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    try {
      const response = await postForm(subtaskCreateUrl, formData, csrfToken);
      if (response.ok) {
        window.location.reload();
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });

  // Toggle Subtask Status
  document.querySelectorAll('.toggle-subtask').forEach(button => {
    button.addEventListener('click', async function() {
      const url = this.dataset.url;
      const isCompleted = this.dataset.completed === 'true';
      const subtaskItem = this.closest('.subtask-item');
      const titleText = subtaskItem.querySelector('.subtask-title-text').textContent;
      const descText = subtaskItem.querySelector('.subtask-description').textContent.trim();
      
      const formData = new FormData();
      formData.append('title', titleText);
      formData.append('description', descText);
      if (!isCompleted) {
        formData.append('is_completed', 'on');
      }

      try {
        const response = await postForm(url, formData, csrfToken);
        if (response.ok) {
          const newCompleted = !isCompleted;
          this.dataset.completed = newCompleted.toString();
          this.textContent = newCompleted ? 'Mark Open' : 'Mark Done';
          this.classList.toggle('btn-success', !newCompleted);
          this.classList.toggle('btn-warning', newCompleted);
          
          const statusBadge = subtaskItem.querySelector('.status');
          statusBadge.textContent = newCompleted ? 'Done' : 'Open';
          statusBadge.classList.toggle('completed', newCompleted);
          statusBadge.classList.toggle('open', !newCompleted);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    });
  });

  // Delete Subtask - Show Modal
  document.querySelectorAll('.delete-subtask').forEach(button => {
    button.addEventListener('click', function() {
      deleteUrl = this.dataset.url;
      deleteSubtaskItem = this.closest('.subtask-item');
      document.getElementById('delete-subtask-title').textContent = this.dataset.title;
      document.getElementById('delete-modal').classList.add('show');
    });
  });

  // Cancel Delete
  document.getElementById('cancel-delete').addEventListener('click', function() {
    document.getElementById('delete-modal').classList.remove('show');
    deleteUrl = null;
    deleteSubtaskItem = null;
  });

  // Confirm Delete
  document.getElementById('confirm-delete').addEventListener('click', async function() {
    if (!deleteUrl || !deleteSubtaskItem) return;
    
    const formData = new FormData();
    
    try {
      const response = await postForm(deleteUrl, formData, csrfToken);
      if (response.ok) {
        deleteSubtaskItem.remove();
        document.getElementById('delete-modal').classList.remove('show');
        
        const remaining = document.querySelectorAll('.subtask-item');
        if (remaining.length === 0) {
          document.getElementById('empty-state').style.display = 'block';
        }
      }
    } catch (error) {
      console.error('Error:', error);
    }
    
    deleteUrl = null;
    deleteSubtaskItem = null;
  });

  // Close modal on background click
  document.getElementById('delete-modal').addEventListener('click', function(e) {
    if (e.target === this) {
      this.classList.remove('show');
      deleteUrl = null;
      deleteSubtaskItem = null;
    }
  });

  // Edit Subtask Forms
  document.querySelectorAll('.edit-subtask-form').forEach(form => {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const url = this.dataset.url;
      const formData = new FormData(this);
      const subtaskItem = this.closest('.subtask-item');
      const statusEl = this.querySelector('.save-status');
      
      const toggleBtn = subtaskItem.querySelector('.toggle-subtask');
      if (toggleBtn.dataset.completed === 'true') {
        formData.append('is_completed', 'on');
      }
      
      try {
        const response = await postForm(url, formData, csrfToken);
        if (response.ok) {
          subtaskItem.querySelector('.subtask-title-text').textContent = formData.get('title');
          subtaskItem.querySelector('.delete-subtask').dataset.title = formData.get('title');
          
          const descEl = subtaskItem.querySelector('.subtask-description');
          const desc = formData.get('description');
          descEl.innerHTML = desc.replace(/\n/g, '<br>');
          descEl.style.display = desc ? 'block' : 'none';
          
          this.closest('details').removeAttribute('open');
          showStatus(statusEl, '✓ Saved!');
        } else {
          showStatus(statusEl, '✗ Error', true);
        }
      } catch (error) {
        showStatus(statusEl, '✗ Error', true);
      }
    });
  });
}