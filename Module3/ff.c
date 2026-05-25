int	ft_atoi_base(const char *str, int str_base)
{
    int i;
    int j;
    int sign;
    int value;
    char *base;

    base = "0123456789abcdef";
    i = 0;
    sign = 1;
    value = 0;
    if (str[i] == '-')
    {
        sign = -1;
        i++;
    }
    while (str[i])
    {
        j = 0;
        while (base[j] && base[j] != str[i] && base[j] != str[i] + 32)
            j++;
        if (!base[j] || j >= str_base)
            break ;
        value = value * str_base + j;
        i++;
    }
    return (value * sign);
}