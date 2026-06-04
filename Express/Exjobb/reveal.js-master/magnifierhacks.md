## Magnifier Hacks ##

🧩 Basic structure (inside your section)

Instead of relying only on data-background-image, you’ll want a real element:

<section id="agenda" class="list">
  <div class="magnifier-lens"></div>
</section>

Then set the background via CSS:

#agenda {
  position: relative;
  background-image: url("./src/agenda_bg.jpg");
  background-size: cover;
  background-position: center;
  overflow: hidden;
}
🔍 Lens styling
.magnifier-lens {
  position: absolute;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  pointer-events: none;

  /* zoom effect */
  background-image: url("./src/agenda_bg.jpg");
  background-repeat: no-repeat;

  /* THIS controls zoom level */
  background-size: 200% 200%;

  /* visual polish */
  box-shadow: 0 0 10px rgba(0,0,0,0.4);
  border: 2px solid rgba(255,255,255,0.6);

  transform: translate(-50%, -50%);
  display: none;
}
⚙️ JavaScript (the actual magnifier logic)
const section = document.querySelector("#agenda");
const lens = document.querySelector(".magnifier-lens");

// adjust this to match zoom level in CSS
const zoom = 2;

section.addEventListener("mouseenter", () => {
  lens.style.display = "block";
});

section.addEventListener("mouseleave", () => {
  lens.style.display = "none";
});

section.addEventListener("mousemove", (e) => {
  const rect = section.getBoundingClientRect();

  // cursor position relative to section
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  // move lens
  lens.style.left = `${x}px`;
  lens.style.top = `${y}px`;

  // move background inside lens (important part)
  const bgX = (x / rect.width) * 100;
  const bgY = (y / rect.height) * 100;

  lens.style.backgroundPosition = `${bgX}% ${bgY}%`;
});
🔥 Why this works
The lens is just a clipped div (circle)
It contains the same image, but zoomed
You “pan” the zoomed image in reverse relative to cursor movement
This gives a real microscope/magnifier feel
🧪 Alternative (more advanced / smoother)

If you want higher fidelity zoom:

Option A: Use a separate high-res image

Instead of scaling the same image, use:

background-image: url("agenda_bg@2x.jpg");

Then keep background-size consistent for crisp zooming.

Option B: Use CSS transform: scale() (less precise)

You can overlay a full image and shift a clipped container, but it’s harder to align correctly.

⚠️ Reveal.js-specific note

Reveal slides sometimes apply transforms (for scaling slides). That can affect coordinate accuracy.

If you see drift:

const rect = section.getBoundingClientRect();

is still correct, but you may need to compensate if Reveal scaling is active:

const scale = Reveal.getScale ? Reveal.getScale() : 1;

and divide coordinates by scale.

🧭 If you want it even cleaner

A more modern pattern is:

background-image on section
a single absolutely-positioned <div class="lens">
lens uses backdrop-filter: none (not needed here, but useful in variants)
