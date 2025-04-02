document.addEventListener("DOMContentLoaded", function () {
    fetchData();  // Fetch initial data

    // Load filters dynamically
    fetch('/api/data')
        .then(response => response.json())
        .then(data => populateFilters(data));
});

// Function to fetch and visualize data
function fetchData(filters = {}) {
    let query = new URLSearchParams(filters).toString();
    let url = "/api/data" + (query ? `?${query}` : '');

    fetch(url)
        .then(response => response.json())
        .then(data => {
            visualizeData(data);
            visualizeLikelihoodRelevance(data);
        });
}

// Populate dropdown filters dynamically
function populateFilters(data) {
    let topics = new Set(), countries = new Set(), regions = new Set(), cities = new Set(),
        endYears = new Set(), sectors = new Set(), pestles = new Set(), sources = new Set(), swots = new Set();

    data.forEach(d => {
        if (d.topic) topics.add(d.topic);
        if (d.country) countries.add(d.country);
        if (d.region) regions.add(d.region);
        if (d.city) cities.add(d.city);
        if (d.end_year) endYears.add(d.end_year);
        if (d.sector) sectors.add(d.sector);
        if (d.pestle) pestles.add(d.pestle);
        if (d.source) sources.add(d.source);
        if (d.swot) swots.add(d.swot);
    });

    populateDropdown("topic-filter", topics);
    populateDropdown("country-filter", countries);
    populateDropdown("region-filter", regions);
    populateDropdown("city-filter", cities);
    populateDropdown("endyear-filter", endYears);
    populateDropdown("sector-filter", sectors);
    populateDropdown("pestle-filter", pestles);
    populateDropdown("source-filter", sources);
    populateDropdown("swot-filter", swots);
}

// Populate dropdown options
function populateDropdown(elementId, values) {
    let select = document.getElementById(elementId);
    values.forEach(value => {
        let option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
}

// Apply filters
function applyFilters() {
    let filters = {};
    let filterIds = ["topic", "country", "region", "city", "endyear", "sector", "pestle", "source", "swot"];

    filterIds.forEach(id => {
        let value = document.getElementById(`${id}-filter`).value;
        if (value) filters[id] = value;
    });

    fetchData(filters);
}

// D3.js Visualization for Intensity
function visualizeData(data) {
    document.getElementById("chart").innerHTML = ""; // Clear existing chart

    const margin = { top: 20, right: 30, bottom: 50, left: 50 };
    const width = 800 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const xScale = d3.scaleBand()
        .domain(data.map(d => d.topic))
        .range([0, width])
        .padding(0.2);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.intensity)])
        .range([height, 0]);

    svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(xScale))
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");

    svg.append("g")
        .call(d3.axisLeft(yScale));

    svg.selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", d => xScale(d.topic))
        .attr("y", d => yScale(d.intensity))
        .attr("width", xScale.bandwidth())
        .attr("height", d => height - yScale(d.intensity))
        .attr("fill", "steelblue");
}

// D3.js Visualization for Likelihood vs. Relevance
function visualizeLikelihoodRelevance(data) {
    document.getElementById("chart-likelihood").innerHTML = "";
    const width = 800, height = 500;

    const svg = d3.select("#chart-likelihood")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const xScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.likelihood)])
        .range([50, width - 50]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.relevance)])
        .range([height - 50, 50]);

    svg.selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", d => xScale(d.likelihood))
        .attr("cy", d => yScale(d.relevance))
        .attr("r", 5)
        .attr("fill", "red");

    svg.append("g")
        .attr("transform", `translate(0, ${height - 50})`)
        .call(d3.axisBottom(xScale));

    svg.append("g")
        .attr("transform", "translate(50, 0)")
        .call(d3.axisLeft(yScale));
}
