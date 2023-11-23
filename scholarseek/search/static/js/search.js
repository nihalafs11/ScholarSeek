document.getElementById('optionsButton').addEventListener('click', function() {
    var options = document.getElementById('optionsCheckbox');
    if (options.style.display === 'none') {
        options.style.display = 'block';
    } else {
        options.style.display = 'none';
    }
});

