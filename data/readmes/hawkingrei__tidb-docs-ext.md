# TiDB Docs Extension for Gemini CLI

This extension provides documentation support for using the TiDB database system within the Gemini CLI environment.

# Extension Installation into Gemini CLI

The easiest way to install this extension is with this command:

```bash
gemini extension install https://github.com/hawkingrei/tidb-docs-ext
```

The command will respond with:

```bash
Extension "tidb-docs-ext" installed successfully and enabled.
```

Alternatively, you can clone this repo directly into your extensions folder.

For global installation:

```bash
mkdir -p ~/.gemini/extensions
git clone https://github.com/hawkingrei/tidb-docs-ext.git ~/.gemini/extensions/tidb-docs-ext
```

For workspace-level installation:

```bash
mkdir -p ./.gemini/extensions
git clone https://github.com/hawkingrei/tidb-docs-ext.git ./.gemini/extensions/tidb-docs-ext
```

Gemini CLI will automatically load the extension on startup and will then use the relevant tools to answer any questions relating to TiDB.
