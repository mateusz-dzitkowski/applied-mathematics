using Graphs
using Plots
using StatsBase

struct Params
    threshold :: AbstractFloat
    profile :: AbstractFloat
    immunization_probability :: AbstractFloat
    spontaneous_adoption :: AbstractFloat
end

struct State
    graph :: Graphs.SimpleGraph
    infected :: AbstractSet
    blocked :: AbstractSet
    params :: Params
end

function get_initial_state(graph :: Graphs.SimpleGraph, params :: Params, percent_initially_infected :: AbstractFloat)
    graph_length = Graphs.nv(graph)
    initially_infected = trunc(Int, graph_length * percent_initially_infected)
    State(
        graph,
        Set(StatsBase.sample(1:graph_length, initially_infected, replace=false)),
        Set(),
        params,
    )
end

function run(state :: State, step_function :: Function, num_steps :: Integer) Vector{Integer}
    infected_count = zeros(Int64, num_steps + 1)
    infected_count[1] = length(state.infected)
    for n = 2:num_steps + 1
        state = step_function(state)
        infected_count[n] = length(state.infected)
    end
    infected_count
end

function run_average(
    graph :: Graphs.SimpleGraph,
    step_function :: Function,
    params :: Params,
    num_steps :: Integer = 30,
    num_runs :: Integer = 20,
)
    output = zeros(Int64, num_steps + 1)
    for n = 1:num_runs
        initial_state = get_initial_state(graph, params, 0.05)
        output += run(initial_state, step_function, num_steps)
    end
    return output / num_runs
end

function profile_model(state::State) State
    new_infected = copy(state.infected)
    for node in Graphs.vertices(state.graph)
        if rand() < state.params.spontaneous_adoption
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

        if rand() >= state.params.profile
            push!(new_infected, node)
        elseif rand() <= state.params.immunization_probability
            push!(state.blocked, node)
        end

    end

    State(state.graph, new_infected, state.blocked, state.params)
end

function profile_threshold_model(state::State) State
    new_infected = copy(state.infected)
    for node in Graphs.vertices(state.graph)
        if rand() < state.params.spontaneous_adoption
            push!(new_infected, node)
            continue
        end

        if in(node, state.infected) || in(node, state.blocked)
            continue
        end

        neighbors = Set(Graphs.neighbors(state.graph, node))
        infected_neighbors = length(intersect(state.infected, neighbors))
        if infected_neighbors == 0
            continue
        end

        if infected_neighbors / length(neighbors) >= state.params.threshold
            if rand() >= state.params.profile
                push!(new_infected, node)
            end
        elseif rand() <= state.params.immunization_probability
            push!(state.blocked, node)
        end

    end

    State(state.graph, new_infected, state.blocked, state.params)
end

function threshold_model(state::State) State
    new_infected = copy(state.infected)
    for node in Graphs.vertices(state.graph)
        if rand() < state.params.spontaneous_adoption
            push!(new_infected, node)
            continue
        end

        if in(node, state.infected)
            continue
        end

        neighbors = Set(Graphs.neighbors(state.graph, node))
        infected_neighbors = length(intersect(state.infected, neighbors))

        if infected_neighbors / length(neighbors) >= state.params.threshold
            push!(new_infected, node)
        end
    end

    State(state.graph, new_infected, state.blocked ,state.params)
end

function main()
    params = Params(0.2, 0.4, 0, 0)
    graph = Graphs.barabasi_albert(63392, 13)

    p = run_average(graph, profile_model, params)
    t = run_average(graph, threshold_model, params)
    pt = run_average(graph, profile_threshold_model, params)

    Plots.savefig(
        Plots.plot(
            [p t pt],
            labels=["profile" "threshold" "profile-threshold"],
            xlabel="Iterations",
            ylabel="Infected nodes",
            legend=:bottomright,
        ),
        "ba_a.pdf",
    )
end

main()
