module ThresholdModel
    using Graphs

    include("State.jl")
    using .State: State

    function step(state::State) State
        new_infected = copy(state.infected)
        for node in Graphs.vertices(state.graph)
            if rand() < state.spontaneous_adoption
                push!(new_infected, node)
                continue
            end

            if in(node, state.infected)
                continue
            end

            neighbors = Set(Graphs.neighbors(state.graph, node))
            infected_neighbors = length(intersect(state.infected, neighbors))

            if infected_neighbors / length(neighbors) >= state.threshold
                push!(new_infected, node)
            end
        end

        State(state.graph, new_infected, state.threshold)
    end

    function run(state::State, k) Vector
        infected_count = Vector()
        push!(infected_count, length(state.infected))
        for _ = 1:k
            state = step(state)
            push!(infected_count, length(state.infected))
        end
        infected_count
    end
end
