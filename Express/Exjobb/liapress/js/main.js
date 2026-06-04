Reveal.on('ready', () => {

  const section = document.querySelector("#frontpage");
  const img = document.querySelector("#bg");
  const lens = document.querySelector(".magnifier-lens");

  const ZOOM = 2;

  section.addEventListener("mouseenter", () => {
    lens.style.display = "block";

    // use the actual image source
    lens.style.backgroundImage = `url(${img.src})`;
  });

  section.addEventListener("mouseleave", () => {
    lens.style.display = "none";
  });

section.addEventListener("mousemove", (e) => {

  const rect = img.getBoundingClientRect();

  const lensRect = lens.getBoundingClientRect();

  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  // move lens (centered on cursor)
  lens.style.left = `${x}px`;
  lens.style.top = `${y}px`;

  const ZOOM = 2;

  // percentage position inside image
  const xPercent = x / rect.width;
  const yPercent = y / rect.height;

  // IMPORTANT: adjust for lens center
  const bgX = (xPercent * rect.width * ZOOM) - (lensRect.width / 2);
  const bgY = (yPercent * rect.height * ZOOM) - (lensRect.height / 2);

  lens.style.backgroundPosition = `${-bgX}px ${-bgY}px`;
  lens.style.backgroundSize = `${rect.width * ZOOM}px ${rect.height * ZOOM}px`;
});

  const walker = document.querySelector("#walker");

  let moving = false;
  let animationFrame = null;

  let x = -300;
  let y = -300;

  function animate() {

    if (!moving) return;

    // move upward-left slowly
    x += 0.35;
    y += 0.35;

    walker.style.right = `${x}px`;
    walker.style.bottom = `${y}px`;

    animationFrame = requestAnimationFrame(animate);
  }

  document.addEventListener("keydown", (e) => {

    if (e.key.toLowerCase() !== "t") return;

    // TOGGLE
    moving = !moving;

    if (moving) {

      animate();

    } else {

      cancelAnimationFrame(animationFrame);

    }

  });


});


/*
Reveal.on('ready', () => {

  const section = document.querySelector("#frontpage");
  const lens = section.querySelector(".magnifier-lens");

  console.log("READY:", section, lens);

  if (!section || !lens) return;

  section.addEventListener("mousemove", (e) => {

    const rect = section.getBoundingClientRect();

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    lens.style.display = "block";
    lens.style.left = x + "px";
    lens.style.top = y + "px";

  });

  section.addEventListener("mouseleave", () => {
    lens.style.display = "none";
  });

});

/*
const section = document.querySelector("#frontpage");
const lens = document.querySelector(".magnifier-lens");

const ZOOM = 2;

section.addEventListener("mouseenter", () => {
  lens.style.display = "block";

  // grab background image from Reveal data attribute
  const bg = section.getAttribute("data-background-image");
  lens.style.backgroundImage = `url(${bg})`;
});

section.addEventListener("mouseleave", () => {
  lens.style.display = "none";
});

section.addEventListener("mousemove", (e) => {
  const rect = section.getBoundingClientRect();

  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  // move lens
  lens.style.left = `${x}px`;
  lens.style.top = `${y}px`;

  // convert to % inside slide
  const xPercent = x / rect.width * 100;
  const yPercent = y / rect.height * 100;

  // shift background inside lens (centered + zoomed)
  const bgX = xPercent * ZOOM;
  const bgY = yPercent * ZOOM;

  lens.style.backgroundPosition = `${bgX}% ${bgY}%`;
  lens.style.backgroundSize = `${rect.width * ZOOM}px ${rect.height * ZOOM}px`;
});
*/
