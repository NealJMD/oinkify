Oinkify
=======

[Oink][1] is a fantastic memory analysis tool for Rails. However, it requires the logs to be formatted with a [Hodel 3000 Compliant logger][2], which prefixes log entries with the PID. I found myself with logs in Rails.logger format that I needed to analyze, so I wrote a brief Python script that transmutes Rails.logger Oink log entries into Hodel 3000 compliant logs. The key is that Oink handily publishes the PID in each log entry, if not on every line.

Usage
-----
```sh
python oinkify.py my_log_file.log --output oink_ready_log.log
bundle exec oink oink_ready_log.log
```

[1]: https://github.com/noahd1/oink
[2]: https://github.com/topfunky/hodel_3000_compliant_logger

License
-------
MIT License