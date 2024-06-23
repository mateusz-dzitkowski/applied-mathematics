module State
    using Graphs

    struct State
        graph :: Graphs.SimpleGraph
        infected :: AbstractSet
        blocked :: AbstractSet
        threshold :: AbstractFloat
        profile :: AbstractFloat
        immunization_probability :: AbstractFloat
        spontaneous_adoption :: AbstractFloat
    end
end