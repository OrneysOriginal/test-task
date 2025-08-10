from reports import Report, ReportFactory


@ReportFactory.register("average")
class AverageReport(Report):
    def generate(self, records):
        endpoint_stats = {}
        for record in records:
            url = record["url"]
            rt = record["response_time"]
            if url not in endpoint_stats:
                endpoint_stats[url] = {"total_requests": 0, "total_response_time": 0.0}
            endpoint_stats[url]["total_requests"] += 1
            endpoint_stats[url]["total_response_time"] += rt

        report_data = []
        for url, stats in endpoint_stats.items():
            avg_rt = stats["total_response_time"] / stats["total_requests"]
            report_data.append((url, stats["total_requests"], round(avg_rt, 3)))

        report_data.sort(key=lambda x: x[1], reverse=True)
        return report_data

    def headers(self):
        return ("handler", "total", "avg_response_time")
