document.addEventListener("DOMContentLoaded", () => {
  async function getMyBoardGames() {
    try {
      const response = await fetch("/api/boardgames/mycollection");
      return await response.json();
    } catch (err) {
      console.log("error", err);
    }
  }

  function renderBoardGames(tableId, games) {
    const bgTable = document.querySelector(tableId);
    let rowNum = 1;
    for (const bg of games) {
      const bgTR = document.createElement("tr");
      const bgRow = document.createElement("th");
      const bgId = document.createElement("td");
      const bgName = document.createElement("td");
      const bgYear = document.createElement("td");

      bgTR.addEventListener("click", addBoardGameRecommendation);
      bgRow.setAttribute("scope", "row");
      bgId.setAttribute("name", "bgId");
      bgName.setAttribute("name", "bgName");
      bgYear.setAttribute("name", "bgYear");

      bgId.style.display = "none";

      bgRow.innerHTML = rowNum;
      bgId.innerHTML = bg.id;
      bgName.innerHTML = bg.name;
      bgYear.innerHTML = bg.year;
      bgTR.append(bgRow, bgId, bgName, bgYear);
      bgTable.append(bgTR);

      rowNum++;
    }
  }

  async function addBoardGameRecommendation(event) {
    const id = event.currentTarget.querySelector("[name=bgId]").textContent;
    const recommendation = { id: id };
    console.log(recommendation);
    try {
      const response = await fetch("/api/boardgames/suggestions", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(recommendation)
      });
      const data = await response.json();
      console.log(data)
    } catch (error) {
      console.log(error);
    }
  }

  async function searchBoardGames(gameName) {
    const url = `/api/boardgames/search/${gameName}`;

    try {
      const response = await fetch(url);
      return await response.json();
    } catch (error) {
      console.log(error);
    }
  }

  async function handleBgSearchForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const bgName = formData.get("name");
    if (bgName) {
      const results = await searchBoardGames(bgName);
      bgTable = document.querySelector("#searchResultTable");
      bgTable.innerHTML = "";
      renderBoardGames("#searchResultTable", results);
    }
  }

  getMyBoardGames().then((data) => renderBoardGames("#boardgame-table", data));

  const bgSearchForm = document.querySelector("#bgsearch-form");
  bgSearchForm.addEventListener("submit", async (e) => handleBgSearchForm(e));
});
