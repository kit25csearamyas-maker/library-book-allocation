import streamlit as st
import heapq

st.set_page_config(page_title="Library Optimizer", layout="wide")
st.title("📚 Library Book Allocation & Transportation System")

# Sample data
if "books" not in st.session_state:
    st.session_state.books = [
        {"id": "B1", "name": "Data Structures", "library": "L1", "stock": 15},
        {"id": "B2", "name": "DAA", "library": "L1", "stock": 12},
        {"id": "B3", "name": "DBMS", "library": "L2", "stock": 8},
        {"id": "B4", "name": "Operating Systems", "library": "L3", "stock": 5}
    ]

if "edges" not in st.session_state:
    st.session_state.edges = {
        "L1": [("L2", 4), ("L3", 2)],
        "L2": [("L1", 4), ("L3", 1)],
        "L3": [("L1", 2), ("L2", 1)]
    }

books = st.session_state.books
menu = st.sidebar.radio("Menu", [
    "Dashboard", "Search Books", "Allocate Books",
    "Shortest Route", "Algorithm Analysis"
])

# Dashboard
if menu == "Dashboard":
    st.subheader("Library Dashboard")
    st.metric("Total Books", sum(b["stock"] for b in books))
    st.dataframe(books, use_container_width=True)

# Search
elif menu == "Search Books":
    query = st.text_input("Enter Book Name or ID").lower()
    result = [b for b in books
              if query and query in (b["name"] + b["id"]).lower()]

    if st.button("Search"):
        if result:
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("Book not found!")

# Book allocation
elif menu == "Allocate Books":
    book = st.selectbox("Select Book", books, format_func=lambda b: b["name"])
    destination = st.selectbox("Destination Library", ["L1", "L2", "L3"])
    quantity = st.number_input("Copies to Transfer", min_value=1, value=1)

    if st.button("Allocate"):
        if destination == book["library"]:
            st.warning("Choose a different library.")
        elif quantity > book["stock"]:
            st.error("Insufficient stock!")
        else:
            book["stock"] -= quantity
            st.success(f"{quantity} copies allocated to {destination}!")
            st.rerun()

# Dijkstra shortest route
elif menu == "Shortest Route":
    start = st.selectbox("Starting Library", ["L1", "L2", "L3"])
    end = st.selectbox("Destination Library", ["L1", "L2", "L3"])

    if st.button("Find Route"):
        distance = {x: float("inf") for x in st.session_state.edges}
        distance[start] = 0
        queue = [(0, start)]
        previous = {}

        while queue:
            cost, node = heapq.heappop(queue)

            if cost > distance[node]:
                continue

            for neighbor, weight in st.session_state.edges[node]:
                new_cost = cost + weight
                if new_cost < distance[neighbor]:
                    distance[neighbor] = new_cost
                    previous[neighbor] = node
                    heapq.heappush(queue, (new_cost, neighbor))

        if distance[end] == float("inf"):
            st.error("No route available.")
        else:
            path = [end]
            while path[-1] != start:
                path.append(previous[path[-1]])
            path.reverse()
            st.success("Route: " + " → ".join(path))
            st.metric("Minimum Cost", distance[end])

# DAA complexity
elif menu == "Algorithm Analysis":
    st.subheader("Algorithm Time Complexity")
    st.table({
        "Algorithm": [
            "Linear Search", "Binary Search", "Merge Sort",
            "0/1 Knapsack DP", "BFS / DFS", "Dijkstra"
        ],
        "Time Complexity": [
            "O(n)", "O(log n)", "O(n log n)",
            "O(nW)", "O(V + E)", "O((V + E) log V)"
        ]
    })