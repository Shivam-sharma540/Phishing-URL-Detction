function toggleSlideBar() {
    const slideBar = document.getElementById("slideBar");
    const toggleBtn = document.querySelector(".toggle-btn");
    
    slideBar.classList.toggle("slide-bar-hidden");
    
    // Change button icon based on state
    if (slideBar.classList.contains("slide-bar-hidden")) {
        toggleBtn.innerHTML = '<i class="fas fa-history"></i> Recently Checked';
    } else {
        toggleBtn.innerHTML = '<i class="fas fa-times"></i> Close';
    }
}

// Close sidebar when clicking outside
document.addEventListener('click', function(event) {
    const slideBar = document.getElementById("slideBar");
    const toggleBtn = document.querySelector(".toggle-btn");
    
    if (!slideBar.contains(event.target) && event.target !== toggleBtn && !slideBar.classList.contains("slide-bar-hidden")) {
        slideBar.classList.add("slide-bar-hidden");
        toggleBtn.innerHTML = '<i class="fas fa-history"></i> Recently Checked';
    }
});

function fillUrlInput(url) {
    document.querySelector('input[name="url"]').value = url;
    document.getElementById("slideBar").classList.add("slide-bar-hidden");
    document.querySelector(".toggle-btn").innerHTML = '<i class="fas fa-history"></i> Recently Checked';
    document.querySelector('input[name="url"]').focus();
}

function clearHistory() {
    if (confirm('Are you sure you want to clear your history?')) {
        fetch('/clear-history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}