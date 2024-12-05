class CupcakeAPI {
  static BASE_URL = "http://localhost:5000/api";

  static async fetchAllCupcakes() {
    const response = await axios.get(`${this.BASE_URL}/cupcakes`);
    return response.data.cupcakes;
  }

  static async createCupcake(data) {
    const response = await axios.post(`${this.BASE_URL}/cupcakes`, data);
    return response.data.cupcake;
  }

  static async deleteCupcake(cupcakeId) {
    await axios.delete(`${this.BASE_URL}/cupcakes/${cupcakeId}`);
  }

  static async searchCupcakes(searchTerm) {
    const response = await axios.get(`${this.BASE_URL}/cupcakes/search?q=${searchTerm}`);
    return response.data.cupcakes;
  }
}

/** given data about a cupcake, generate HTML */
function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}

// Example usage
$(async function() {
  const cupcakes = await CupcakeAPI.fetchAllCupcakes();
  for (let cupcake of cupcakes) {
    $("#cupcakes-list").append(generateCupcakeHTML(cupcake));
  }

  $("#new-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val() || 'https://tinyurl.com/demo-cupcake';

    console.log("Form Data:", { flavor, rating, size, image });  // Debugging line

    try {
      const newCupcakeResponse = await axios.post(`${CupcakeAPI.BASE_URL}/cupcakes`, {
        flavor: flavor,
        rating: rating,
        size: size,
        image: image
      });

      console.log("Response Data:", newCupcakeResponse.data);  // Debugging line

      let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
      $("#cupcakes-list").append(newCupcake);
      $("#new-cupcake-form").trigger("reset");
    } catch (err) {
      console.error("Error adding new cupcake:", err);
      console.error("Error Response:", err.response);  // More detailed error info
      alert("Could not add cupcake. Please try again later.");
    }
  });

  $("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    const $cupcake = $(evt.target).closest("div");
    const cupcakeId = $cupcake.attr("data-cupcake-id");

    await CupcakeAPI.deleteCupcake(cupcakeId);
    $cupcake.remove();
  });
});
