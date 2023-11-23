function togglePopup() {
    var popup = document.getElementById("optionsPopup");
    popup.style.display = popup.style.display === 'none' ? 'block' : 'none';
}

// Wait for the DOM to be loaded
document.addEventListener("DOMContentLoaded", function() {
    // Attach the function to the button
    document.getElementById("optionsButton").addEventListener("click", togglePopup);
});