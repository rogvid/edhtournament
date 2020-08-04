import React from "react";
import axios from "axios";
import "./App.css";

function handleSubmit(event) {
    const text = document.querySelector("#char-input").value;

    axios
        .get(`/api/players`)
        .then(({ data }) => {
            document.querySelector(
                "#char-count"
            ).textContent = `${data.count} characters!`;
        })
        .catch(err => console.log(err));
}

function App() {
    return (
            <div className="App">
            <div>
            <button onClick={getPlayers}>Players</button>
            </div>
            <div>
            <h3 id="Pl"></h3>
            </div>
            </div>
    );
}

export default App;
