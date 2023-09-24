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
      const bgName = document.createElement("td");
      const bgYear = document.createElement("td");

      bgRow.setAttribute("scope", "row");

      bgRow.innerHTML = rowNum;
      bgName.innerHTML = bg.name;
      bgYear.innerHTML = bg.year;
      bgTR.append(bgRow, bgName, bgYear);
      bgTable.append(bgTR);

      rowNum++;
    }
  }

  async function searchBoardGames(formData) {
    const url = "/api/boardgames/search";

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      return await response.json();
    } catch (error) {
      console.log(error);
    }
  }

  async function handleBgSearchForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    if (formData.get("name")) {
      const results = await searchBoardGames(formData);
      bgTable = document.querySelector("#searchResultTable");
      renderBoardGames("#searchResultTable", results);
    }
  }

  getMyBoardGames().then((data) => renderBoardGames("#boardgame-table", data));

  const bgSearchForm = document.querySelector("#bgsearch-form");
  bgSearchForm.addEventListener("submit", async (e) => handleBgSearchForm(e));
});
