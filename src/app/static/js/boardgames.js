document.addEventListener("DOMContentLoaded", () => {
  const bgCollectionEndpoint = "/api/boardgames/mycollection";
  const bgSuggestionEndpoint = "/api/boardgames/suggestions";
  const bgSearchEndpoint = (gameId) => `/api/boardgames/search/${gameId}`;
  const bgCollectionTable = document.querySelector("#bgCollectionTable");
  const bgSearchResultTable = document.querySelector("#bgSearchResultTable");
  const bgSuggestionsTable = document.querySelector("#bgSuggestionsTable");
  const bgSearchForm = document.querySelector("#bgSearchForm");
  const bgSuggestForm = document.querySelector("#bgSuggestForm");
  const bgSuggestSubmit = document.querySelector("#submitSuggestion");
  const getRecommendationRow = () =>
    bgSearchResultTable.querySelector("tr[selected]");
  const updateSuggestSubmit = () =>
    (bgSuggestSubmit.disabled = !getRecommendationRow());
  const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));

  async function getMyBoardGames() {
    try {
      const response = await fetch(bgCollectionEndpoint);
      return await response.json();
    } catch (err) {
      console.log("error", err);
    }
  }

  async function getSuggestions() {
    try {
      const response = await fetch(bgSuggestionEndpoint);
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

  async function renderBoardGames(bgTable, games) {
    const gamesToTRs = new Map();
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

      gamesToTRs.set(bg, bgTR);

      rowNum++;
    }

    return gamesToTRs;
  }

  async function renderSuggestions(suggestions) {
    const gamesToTRs = await renderBoardGames(bgSuggestionsTable, suggestions);

    for (const [bg, bgRow] of gamesToTRs.entries()) {
      const bgCount = document.createElement("td");
      bgCount.setAttribute("name", "bgCount");
      bgCount.innerHTML = bg.count;

      bgRow.append(bgCount);
    }

    return gamesToTRs;
  }

  async function updateMyCollectionTable() {
    await getMyBoardGames().then((games) =>
      renderBoardGames(bgCollectionTable, games)
    );
  }

  async function updateSuggestionsTable() {
    await getSuggestions().then((games) => renderSuggestions(games));
  }

  async function addBgRecommendation(gameId) {
    const recommendation = { value: gameId };
    try {
      const response = await fetch(bgSuggestionEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(recommendation),
      });
      await response.json();
      await updateSuggestionsTable();
    } catch (error) {
      console.log(error);
    }
  }

  async function selectBgSearchResultItem(event) {
    const previousSelection = getRecommendationRow();

    event.currentTarget.setAttribute("selected", "");

    if (previousSelection) {
      previousSelection.removeAttribute("selected");
    }
  }

  async function handleBgSearchSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const bgName = formData.get("name");
    if (bgName) {
      const results = await searchBoardGames(bgName);
      const bgMap = await renderBoardGames(bgSearchResultTable, results);
      for (const bgRow of bgMap.values()) {
        bgRow.addEventListener("mousedown", (e) => {
          if (e.button == 0) selectBgSearchResultItem(e);
          updateSuggestSubmit();
        });
      }
    }
  }

  async function handleBgSuggestSubmit(event) {
    event.preventDefault();
    const id = getRecommendationRow().querySelector("[name=bgId]").textContent;
    getRecommendationRow().removeAttribute("selected");
    updateSuggestSubmit();
    bgSuggestSubmit.value = "Sending...";
    await addBgRecommendation(id);
    bgSuggestSubmit.value = "Thank you!";
    await sleep(2000);
    bgSuggestSubmit.value = "Send Suggestion";
  }

  updateMyCollectionTable();
  updateSuggestionsTable();

  bgSearchForm.addEventListener("submit", async (e) => handleBgSearchSubmit(e));
  bgSuggestForm.addEventListener("submit", (e) => handleBgSuggestSubmit(e));
});
