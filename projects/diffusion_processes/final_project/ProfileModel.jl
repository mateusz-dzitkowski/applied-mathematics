module ProfileModel
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

            if in(node, state.infected) || in(node, state.blocked)
                continue
            end

            neighbors = Set(Graphs.neighbors(state.graph, node))
            infected_neighbors = intersect(state.infected, neighbors)
            if length(infected_neighbors) == 0
                continue
            end

            if rand() >= state.profile
                push!(new_infected, node)
            elseif rand() <= state.immunization_probability
                push!(state.blocked, node)
            end

        end

        State(state.graph, new_infected, state.blocked, state.profile, state.immunization_probability)
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
