document.addEventListener("DOMContentLoaded", function () {
    // Get all the dropdown menu elements
    var dropdownMenus = document.querySelectorAll(".dropdown-menu");

    // Get all the dropdown toggle buttons
    var dropdownButtons = document.querySelectorAll(".dropdown-toggle");

    // Function to toggle a specific dropdown menu
    function toggleDropdown(index) {
        dropdownMenus.forEach(function (menu, i) {
            if (i !== index) {
                menu.classList.remove("show");
            }
        });

        dropdownMenus[index].classList.toggle("show");
    }

    // Event listener to show/hide the dropdown menu when the button is clicked
    dropdownButtons.forEach(function (button, index) {
        button.addEventListener("click", function () {
            toggleDropdown(index);
        });
    });

    // Event listener to hide the dropdown menus when clicking outside the menus or the buttons
    window.addEventListener("click", function (event) {
        if (!event.target.matches(".dropdown-toggle") && !event.target.matches(".dropdown-item")) {
            dropdownMenus.forEach(function (menu) {
                menu.classList.remove("show");
            });
        }
    });
});