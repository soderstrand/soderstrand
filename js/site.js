// =====================================================
// Soderstrand Personal Website
// Shared Components Prototype
// =====================================================

document.addEventListener("DOMContentLoaded", async function () {

    const siteRoot = "/soderstrand";

    async function loadComponent(id, file) {
        const target = document.getElementById(id);
        if (!target) return;

        const response = await fetch(siteRoot + "/shared/" + file);
        if (!response.ok) {
            console.error("Unable to load:", siteRoot + "/shared/" + file);
            return;
        }

        target.innerHTML = await response.text();

        if (id === "nav") {
            document.querySelectorAll("#nav a").forEach(link => {
                const href = link.getAttribute("href");
                link.href = siteRoot + "/" + href;

                const current = window.location.pathname;
                if (current.endsWith(href) ||
                    (href === "story/story.html" && current.includes("/story/"))) {
                    link.classList.add("active");
                }
            });
        }
    }

    await loadComponent("header","header.html");
    await loadComponent("nav","nav.html");
    await loadComponent("footer","footer.html");
});
