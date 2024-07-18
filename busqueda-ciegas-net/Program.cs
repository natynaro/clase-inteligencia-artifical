// See https://aka.ms/new-console-template for more information

using busqueda_ciegas_net;

Console.WriteLine("Hello, World!");

List<Operator<(Jarra j1, Jarra j2)>> operators =
[
    new Operator<(Jarra j1, Jarra j2)>("llenar jarra de 3 litros") { Func = j => (3, j.j2) },
    new Operator<(Jarra j1, Jarra j2)>("llenar jarra de 4 litros") { Func = j => (j.j1, 4)},
    new Operator<(Jarra j1, Jarra j2)>("vaciar jarra de 3 litros") { Func = j => (0, j.j2)},
    new Operator<(Jarra j1, Jarra j2)>("vaciar jarra de 4 litros") { Func = j => (j.j2, 0)},
    new Operator<(Jarra j1, Jarra j2)>("pasar a jarra 4 litros") { Func = j => (j.j2, 0)},
    new Operator<(Jarra j1, Jarra j2)>("pasar a jarra 3 litros") { Func = j => (j.j2, 0)},
];


class Jarra
{
    public int Cantidad { get; init; }
    public static implicit operator Jarra(int i) => new() { Cantidad = i };

    public static void Pasar(int c1, Jarra j1, int c2, Jarra j2)
    {
        var diff = Math.Min()
    }
}