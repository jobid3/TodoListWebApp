let deleteUrl = null;
let deleteTaskItem = null;

// Helper function for POST requests
async function postForm(url, formData, csrfToken) {
  formData.append('csrfmiddlewaretoken', csrfToken);
  const response = await fetch(url, {
    method: 'POST',
    body: formData
  });
  return response;
}

function initTaskList(config) {
  const { csrfToken } = config;

  // Toggle Task Status
  document.querySelectorAll('.toggle-task').forEach(button => {
    button.addEventListener('click', async function() {
      const url = this.dataset.url;
      const title = this.dataset.title;
      const description = this.dataset.description;
      const isCompleted = this.dataset.completed === 'true';
      
      const formData = new FormData();
      formData.append('title', title);
      formData.append('description', description);
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
          
          const taskItem = this.closest('.task-item');
          const statusBadge = taskItem.querySelector('.status');
          statusBadge.textContent = newCompleted ? 'Completed' : 'Open';
          statusBadge.classList.toggle('completed', newCompleted);
          statusBadge.classList.toggle('open', !newCompleted);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    });
  });

  // Delete Task - Show Modal
  document.querySelectorAll('.delete-task').forEach(button => {
    button.addEventListener('click', function() {
      deleteUrl = this.dataset.url;
      deleteTaskItem = this.closest('.task-item');
      document.getElementById('delete-task-title').textContent = this.dataset.title;
      document.getElementById('delete-modal').classList.add('show');
    });
  });

  // Cancel Delete
  document.getElementById('cancel-delete').addEventListener('click', function() {
    document.getElementById('delete-modal').classList.remove('show');
    deleteUrl = null;
    deleteTaskItem = null;
  });

  // Confirm Delete
  document.getElementById('confirm-delete').addEventListener('click', async function() {
    if (!deleteUrl || !deleteTaskItem) return;
    
    const formData = new FormData();
    
    try {
      const response = await postForm(deleteUrl, formData, csrfToken);
      if (response.ok) {
        deleteTaskItem.remove();
        document.getElementById('delete-modal').classList.remove('show');
        
        // Show empty state if no tasks left
        const remaining = document.querySelectorAll('.task-item');
        if (remaining.length === 0) {
          document.querySelector('.task-list').remove();
          const emptyState = document.createElement('div');
          emptyState.className = 'card empty-state';
          emptyState.innerHTML = `
            <div class="empty-state-icon">📝</div>
            <h2>No tasks yet</h2>
            <p>Add your first task above to get started!</p>
          `;
          document.querySelector('.container').appendChild(emptyState);
        }
      }
    } catch (error) {
      console.error('Error:', error);
    }
    
    deleteUrl = null;
    deleteTaskItem = null;
  });

  // Close modal on background click
  document.getElementById('delete-modal').addEventListener('click', function(e) {
    if (e.target === this) {
      this.classList.remove('show');
      deleteUrl = null;
      deleteTaskItem = null;
    }
  });
}