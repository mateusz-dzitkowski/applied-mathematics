using Graphs
using Plots
using StatsBase

struct Params
    threshold :: AbstractFloat
    profile :: AbstractFloat
    immunization_probability :: AbstractFloat
    spontaneous_adoption :: AbstractFloat
    cure :: AbstractFloat
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
    num_runs :: Integer = 10,
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

function profile_threshold_cure_model(state :: State)
    # a model with an additional chance for each node to be spontaneously cured (not immunized)
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

    for node in state.infected
        if rand() <= state.params.cure
            delete!(new_infected, node)
        end
    end

    State(state.graph, new_infected, state.blocked, state.params)
end

function run_and_save_fig(graph :: Graphs.SimpleGraph, params :: Params, file_name :: String)
    p = run_average(graph, profile_model, params)
    t = run_average(graph, threshold_model, params)
    pt = run_average(graph, profile_threshold_model, params)
    ptc = run_average(graph, profile_threshold_cure_model, params)
    Plots.savefig(
        Plots.plot(
            [p t pt ptc],
            labels=["profile" "threshold" "profile-threshold" "profile-threshold-cure"],
            xlabel="Iterations",
            ylabel="Infected nodes",
            legend=:bottomright,
            legendcolumns=2,
        ),
        file_name,
    )
end

function main()
    n = 63392

    graphs = (
        ("BA", Graphs.barabasi_albert(n, 13)),
        ("ER", Graphs.erdos_renyi(n, 0.0004)),
        ("WS", Graphs.watts_strogatz(n, 13, 0.01)),
    )
    params_s = (
        ("a", Params(0.1, 0.8, 0, 0, 0)),
        ("b", Params(0.1, 0.8, 0.05, 0, 0)),
        ("c", Params(0.1, 0.8, 0.05, 0.005, 0)),
        ("d", Params(0.1, 0.8, 0.05, 0.005, 0.05)),
    )

    for ((graph_name, graph), (params_name, params)) in Iterators.product(graphs, params_s)
        file_name = graph_name * "_" * params_name * ".pdf"
        run_and_save_fig(graph, params, file_name)
        println("DONE: " * file_name)
    end
end

main()
