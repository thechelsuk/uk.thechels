// Homepage post-type filter: icon links in the count line. Each is a link to that type's archive page; with
// JavaScript on, it filters the homepage list in place, rewrites the count ("278 ride posts // full archive") and
// keeps the choice in the address (?type=ride), so Back undoes it and a filtered view can be shared.
(function () {
    "use strict";
    const tabs = document.querySelector(".type-filter");
    const list = document.getElementById("blog-archives");
    const meta = document.querySelector(".page-meta--home");
    if (!tabs || !list || !meta) return;

    const rows = Array.from(list.querySelectorAll(".posts[data-type]"));
    const headings = Array.from(list.querySelectorAll("h2"));
    const skip = list.querySelector(".year-skip");
    const count = meta.querySelector(".page-meta__count");
    const allTab = tabs.querySelector('a[data-type="all"]');

    function tabFor(type) {
        return tabs.querySelector(`a[data-type="${type}"]`);
    }

    function setMeta(tab, all) {
        count.innerHTML = "";
        const b = document.createElement("b");
        b.textContent = tab.dataset.count;
        count.append(b, ` ${tab.dataset.noun}`);
        let links = meta.querySelector(".page-meta__links");
        if (links) links.remove();
        if (all) return;
        links = document.createElement("span");
        links.className = "page-meta__links";
        const sep = document.createElement("span");
        sep.className = "page-meta__sep";
        sep.setAttribute("aria-hidden", "true");
        sep.textContent = "//";
        const archive = document.createElement("a");
        archive.href = tab.getAttribute("href");
        archive.textContent = "full archive";
        links.append(sep, archive);
        count.append(" ", links);
    }

    function apply(type) {
        const tab = tabFor(type) || allTab;
        const all = tab === allTab;
        rows.forEach((row) => {
            row.hidden = !(all || row.dataset.type === tab.dataset.type);
        });
        // Hide a year heading when none of the rows under it are showing.
        headings.forEach((h2) => {
            let el = h2.nextElementSibling;
            let any = false;
            while (el && el.tagName !== "H2") {
                if (el.matches(".posts[data-type]") && !el.hidden) any = true;
                el = el.nextElementSibling;
            }
            h2.hidden = !all && !any;
        });
        if (skip) skip.hidden = !all;
        tabs.querySelectorAll("a").forEach((a) => {
            if (a === tab) a.setAttribute("aria-current", "true");
            else a.removeAttribute("aria-current");
        });
        setMeta(tab, all);
    }

    function typeFromUrl() {
        return new URLSearchParams(window.location.search).get("type") || "all";
    }

    function onClick(event) {
        const link = event.target.closest("a[data-type]");
        if (!link || event.metaKey || event.ctrlKey || event.shiftKey) return;
        event.preventDefault();
        const type = link.dataset.type;
        const url = type === "all" ? window.location.pathname : `?type=${encodeURIComponent(type)}`;
        window.history.pushState({ type }, "", url);
        apply(type);
    }

    tabs.addEventListener("click", onClick);
    meta.addEventListener("click", onClick);
    window.addEventListener("popstate", () => apply(typeFromUrl()));
    if (typeFromUrl() !== "all") apply(typeFromUrl());
})();
