function update() {
  pywebview.api
    .get_info()
    .then(function (d) {
      var st = document.getElementById("status");
      st.textContent = d.running ? "🟢 En línea" : "🔴 Detenido";
      st.className = "badge " + (d.running ? "on" : "off");

      document.getElementById("uptime").textContent = d.uptime || "-";
      document.getElementById("last").textContent = d.last_interaction;

      var el = document.getElementById("events");
      el.innerHTML =
        d.events && d.events.length ? d.events.join("<br>") : "Sin eventos";
      el.scrollTop = el.scrollHeight;
    })
    .catch(function () {});
}

setInterval(update, 1500);
update();
