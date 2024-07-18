namespace busqueda_ciegas_net;

public class Tree<T> where T : notnull
{
    public required Node<T> Root { get; init; }
    public required T ObjectiveState { get; init; }
    public required List<Operator<T>> Operators { get; init; }

    public static void BreadthFirst(T initialState, T objectiveState, IEnumerable<Operator<T>> operators)
    {
        var ops = operators.ToList();
        var tree = new Tree<T>
        {
            Root = new Node<T>
            {
                State = initialState,
                Operators = ops.ToList(),
            },
            ObjectiveState = objectiveState,
            Operators = ops.ToList()
        };
    }

    public static void BreadthFirst(Tree<T> tree)
    {
        Node<T>? r = null;
        var queue = new Queue<Node<T>>();
        queue.Enqueue(tree.Root);

        while (queue.Count != 0)
        {
            var node = queue.Dequeue();
            if (node.State.Equals(tree.ObjectiveState))
            {
                r = node;
                break;
            }

            var children = node.CreateChildren();
            foreach (var n in children)
            {
                node.Add(in n);
                queue.Enqueue(n);
            }
        }

        if (r is not null)
        {
            Console.WriteLine(r.PathToRoot());
        }
        else
        {
            Console.WriteLine("Solution not found");
        }
    }
}