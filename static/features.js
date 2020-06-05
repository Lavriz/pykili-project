$(document).ready(function() {
  var textWrapper = document.querySelector('.move');
  textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");
  anime.timeline({loop: 1})
    .add({
      targets: '.move .letter',
      opacity: [0,1],
      easing: "easeInOutQuad",
      duration: 800,
      delay: (el, i) => 150 * (i+1)
    });
});
