# 说明
为了方便展示 bytes 数组，程序中用了 52 个英文字母。

# 本人的测试环境
CPU: Intel Core i7, 2GHz, 4 核心

# 性能结果
 使用 goroutine 并发，~6.37s；不使用 goroutine 并发，~22.21s.
 调试时显示：2 路并发，~44s; 4 路并发，~22s; 8 路并发，~14.7s; 16 路并发，~11s; 32 路并发，~9s; 64 路并发，~7.6s; 128 路并发，~6.37s。
 随着并发度2倍提升，时间并没有保持减半。这里的原因是受到 4 核 cpu 限制。

# 测试结果展示

App elapsed:  6.365098486s
TargetKey:  JtddxJXtSsbqjHXgCTDoARvPuHrxqYXuUKPANhctdQZYByMCdcNdUbYPropkBMFQuNbqomhMacNyClWyOtiDppQqIcKZeBwSNhIrSwxQDNsyKfsLaEDSpCCFcMptAEbxTnGRTBmpFsHUGSzqUlqhKEyfntwHXHNIwCFNRjFuSpffDQoLjPUdLDCgYJNapQeWeknLWabxGyeYIxVXRUOWAMEkqoBRFtGyZJunxTJfCSnQuDUMHJCerbAoOSyTthRX
Result:     JtddxJXtSsbqjHXgCTDoARvPuHrxqYXuUKPANhctdQZYByMCdcNdUbYPropkBMFQuNbqomhMacNyClWyOtiDppQqIcKZeBwSNhIrSwxQDNsyKfsLaEDSpCCFcMptAEbxTnGRTBmpFsHUGSzqUlqhKEyfntwHXHNIwCFNRjFuSpffDQoLjPUdLDCgYJNapQeWeknLWabxGyeYIxVXRUOWAMEkqoBRFtGyZJunxTJfCSnQuDUMHJCerbAoOSyTthRX
