(function () {
  var figures = document.querySelectorAll("main img");
  if (!figures.length) return;

  var isFr = (document.documentElement.lang || "").toLowerCase().indexOf("fr") === 0;
  var closeLabel = isFr ? "Fermer" : "Close";

  var overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.setAttribute("hidden", "");
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", isFr ? "Aperçu de l’image" : "Image preview");
  overlay.innerHTML =
    '<button type="button" class="lightbox-close" aria-label="' + closeLabel + '">&times;</button>' +
    '<img class="lightbox-image" alt="">';
  document.body.appendChild(overlay);

  var lightImg = overlay.querySelector(".lightbox-image");
  var closeBtn = overlay.querySelector(".lightbox-close");
  var lastFocus = null;

  function openLightbox(src, alt) {
    lastFocus = document.activeElement;
    lightImg.src = src;
    lightImg.alt = alt || "";
    overlay.removeAttribute("hidden");
    document.body.classList.add("lightbox-open");
    closeBtn.focus();
  }

  function closeLightbox() {
    overlay.setAttribute("hidden", "");
    document.body.classList.remove("lightbox-open");
    lightImg.removeAttribute("src");
    lightImg.alt = "";
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  figures.forEach(function (img) {
    if (img.classList.contains("way-icon")) return;
    if (img.closest(".paypal-btn") || img.closest("button") || img.closest("a.social-link")) return;

    img.classList.add("lightbox-trigger");
    img.setAttribute("tabindex", "0");
    img.setAttribute("role", "button");
    if (!img.getAttribute("aria-label")) {
      img.setAttribute(
        "aria-label",
        isFr ? "Agrandir l’image" : "View larger image"
      );
    }

    function activate(e) {
      e.preventDefault();
      openLightbox(img.currentSrc || img.src, img.alt || "");
    }

    img.addEventListener("click", activate);
    img.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        activate(e);
      }
    });
  });

  closeBtn.addEventListener("click", closeLightbox);
  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) closeLightbox();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !overlay.hasAttribute("hidden")) {
      closeLightbox();
    }
  });
})();
