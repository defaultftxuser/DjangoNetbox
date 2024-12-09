document.addEventListener("DOMContentLoaded", function () {
    const addressInput = document.getElementById("id_address");

    if (addressInput) {
        let timeout = null;

        addressInput.addEventListener("input", function () {
            const query = addressInput.value;

            if (timeout) {
                clearTimeout(timeout);
            }

            timeout = setTimeout(() => {
                if (query.length > 2) {
                    fetch(`/api/dadata/suggest/?query=${encodeURIComponent(query)}`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.suggestions) {
                                let datalist = document.getElementById("address-suggestions");
                                if (!datalist) {
                                    datalist = document.createElement("datalist");
                                    datalist.id = "address-suggestions";
                                    addressInput.setAttribute("list", "address-suggestions");
                                    document.body.appendChild(datalist);
                                }
                                datalist.innerHTML = "";

                                data.suggestions.forEach(suggestion => {
                                    const option = document.createElement("option");
                                    option.value = suggestion.value;
                                    datalist.appendChild(option);
                                });
                            }
                        })
                        .catch(error => {
                            console.error("Error fetching suggestions:", error);
                        });
                }
            }, 300);
        });
    }
});
