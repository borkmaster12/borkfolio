document.addEventListener("DOMContentLoaded", () => {
  const bgCollectionEndpoint = "/api/boardgames/mycollection";
  const bgSuggestionEndpoint = "/api/boardgames/suggestions";
  const bgSearchEndpoint = (gameId) => `/api/boardgames/search/${gameId}`;
  const bgCollectionTable = document.querySelector("#bgCollectionTable");
  const bgSearchResultTable = document.querySelector("#bgSearchResultTable");
  const bgSearchForm = document.querySelector("#bgSearchForm");
  const bgSuggestForm = document.querySelector("#bgSuggestForm");
  const bgSuggestSubmit = document.querySelector("#submitSuggestion");
  const getRecommendationRow = () =>
    bgSearchResultTable.querySelector("tr[selected]");

  async function getMyBoardGames() {
    try {
      const response = await fetch(bgCollectionEndpoint);
      return await response.json();
    } catch (err) {
      console.log("error", err);
    }
  }

  async function searchBoardGames(gameName) {
    const url = bgSearchEndpoint(gameName);

    try {
      const response = await fetch(url);
      return await response.json();
    } catch (error) {
      console.log(error);
    }
  }

  function renderBoardGames(bgTable, games) {
    const bgRows = [];
    let rowNum = 1;

    bgTable.innerHTML = "";

    for (const bg of games) {
      const bgTR = document.createElement("tr");
      const bgRow = document.createElement("th");
      const bgId = document.createElement("td");
      const bgName = document.createElement("td");
      const bgYear = document.createElement("td");

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

      bgRows.push(bgTR);

      rowNum++;
    }

    return bgRows;
  }

  function selectBgSearchResultItem(event) {
    const previousSelection = getRecommendationRow();

    event.currentTarget.setAttribute("selected", "");

    if (previousSelection) {
      previousSelection.removeAttribute("selected");
    }
  }

  async function addBgRecommendation(gameId) {
    const recommendation = { id: gameId };
    try {
      const response = await fetch(bgSuggestionEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(recommendation),
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.log(error);
    }
  }

  async function handleBgSearchSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const bgName = formData.get("name");
    if (bgName) {
      const results = await searchBoardGames(bgName);
      const bgRows = renderBoardGames(bgSearchResultTable, results);
      for (const bgRow of bgRows) {
        bgRow.addEventListener("mousedown", async (e) => {
          if (e.button == 0) selectBgSearchResultItem(e);
          bgSuggestSubmit.disabled = !getRecommendationRow();
        });
      }
    }
  }

  async function handleBgSuggestSubmit(event) {
    event.preventDefault();
    const id = getRecommendationRow().querySelector("[name=bgId]").textContent;
    await addBgRecommendation(id);
  }

  getMyBoardGames().then((games) => renderBoardGames(bgCollectionTable, games));
  bgSearchForm.addEventListener("submit", async (e) => handleBgSearchSubmit(e));
  bgSuggestForm.addEventListener("submit", async (e) =>
    handleBgSuggestSubmit(e)
  );
});
