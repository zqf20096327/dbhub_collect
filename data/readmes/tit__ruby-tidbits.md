# Tidbits

This is my personal library I use to share the Ruby tidbits I made it for my various projects

## Installation

Add this line to your application's Gemfile:

```ruby
gem 'ruby-tidbits', git: 'https://github.com/konoplev-roman/ruby-tidbits'
```

And then execute:

    $ bundle

## Usage

To use bool extensions, add to the top of your file:

    require 'tidbits/bool'

You can now use 
* `.to_bool` on `NilClass`, `String`, `Numeric`, `FalseClass`
and `TrueClass`
* `.to_i` for `FalseClass` and `TrueClass`

Example:

    nil.to_bool
    # => false

    'yes'.to_bool
    # => true

    'no'.to_bool
    # => false

    1.to_bool
    # => true

    0.to_bool
    # => false

    false.to_bool
    # => false

    false.to_i
    # => 0

    false.to_bool
    # => true

    true.to_i
    # => 1

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/konoplev-roman/ruby-tidbits. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.

## License

The gem is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).

## Code of Conduct

Everyone interacting in the Ruby::Tidbits project’s codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](https://github.com/konoplev-roman/ruby-tidbits/blob/master/CODE_OF_CONDUCT.md).
