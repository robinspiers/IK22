var button = document.querySelector('button');
for (var i = button.children.length; i >= 0; i--) {
    button.appendChild(button).children[Math.random() * i | 0]);
}