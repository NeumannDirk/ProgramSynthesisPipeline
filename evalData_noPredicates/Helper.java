
public class Helper {
	public static int pow2(int a, int b) {
		if (b == 0)
			return 1;
		int res = a;
		for (int i = 0; i < b - 1; i++) {
			res *= a;
		}
		return res;
	}

	public static int factorial2(int x) {
		if (x <= 0)
			return 1;
		else
			return x * factorial2(x - 1);
	}
}
