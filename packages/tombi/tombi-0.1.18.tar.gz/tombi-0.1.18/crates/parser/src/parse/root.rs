use crate::{parser::Parser, token_set::TS_KEY_FIRST};

use super::{
    begin_dangling_comments, end_dangling_comments, invalid_line, leading_comments,
    peek_leading_comments, tailing_comment, Parse, TS_LINE_END,
};
use crate::ErrorKind::*;
use syntax::{SyntaxKind::*, T};

impl Parse for ast::Root {
    fn parse(p: &mut Parser<'_>) {
        let m = p.start();

        begin_dangling_comments(p);

        loop {
            let n = peek_leading_comments(p);
            if p.nth_at(n, EOF) {
                break;
            } else if p.nth_at_ts(n, TS_KEY_FIRST) {
                ast::KeyValue::parse(p);
                if !p.at_ts(TS_LINE_END) {
                    invalid_line(p, ExpectedLineBreak);
                }
            } else if p.nth_at(n, T!("[[")) {
                ast::ArrayOfTables::parse(p);
            } else if p.nth_at(n, T!['[']) {
                ast::Table::parse(p);
            } else {
                unknwon_line(p);
            }
        }

        end_dangling_comments(p, true);

        m.complete(p, ROOT);
    }
}

fn unknwon_line(p: &mut Parser<'_>) {
    let m = p.start();

    leading_comments(p);

    while !p.at_ts(TS_LINE_END) {
        p.bump_any();
    }
    p.error(crate::Error::new(UnknownLine, p.current_range()));

    tailing_comment(p);

    m.complete(p, ERROR);
}

#[cfg(test)]
mod test {
    #[test]
    fn test_begin_dangling_comments() {
        let input = r#"
# begin dangling_comment1
# begin dangling_comment2

# table leading comment1
# table leading comment2
[table]
        "#
        .trim();
        let p = crate::parse(input, crate::TomlVersion::default());

        assert_eq!(p.errors(), vec![]);
    }
}
