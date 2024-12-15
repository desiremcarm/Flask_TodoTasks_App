let taskToDelete = null;

function setTaskId(task_id) {
  taskToDelete = task_id; // Save task ID
  document.getElementById("dialog").open = true; // Open modal
  document.getElementById("delBtn").href = "/del/" + taskToDelete; // Set the delete button of the modal
}

function closeDialog() {
  document.getElementById("dialog").open = false; // Close modal
}
